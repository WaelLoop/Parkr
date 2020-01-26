# -*- coding: utf-8 -*- #
# Copyright 2019 Google LLC. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Command for running a local development environment."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import contextlib
import os.path
import signal
import subprocess
import sys
import tempfile

from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.code import flags
from googlecloudsdk.command_lib.code import kube_context
from googlecloudsdk.command_lib.code import local
from googlecloudsdk.command_lib.code import local_files
from googlecloudsdk.core import config
from googlecloudsdk.core.updater import update_manager
from googlecloudsdk.core.util import files as file_utils
from googlecloudsdk.core.util import platforms
import six

DEFAULT_CLUSTER_NAME = 'gcloud-local-dev'


def _EmptyHandler(unused_signum, unused_stack):
  """Do nothing signal handler."""
  pass


class _SigInterruptedHandler(object):
  """Context manager to capture CTRL-C and send it to a handler."""

  def __init__(self, handler):
    self._orig_handler = None
    self._handler = handler

  def __enter__(self):
    self._orig_handler = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGINT, self._handler)

  def __exit__(self, exc_type, exc_value, tb):
    signal.signal(signal.SIGINT, self._orig_handler)


def _FindOrInstallSkaffoldComponent():
  if (config.Paths().sdk_root or
      update_manager.EnsureInstalledAndRestart(['skaffold'])):
    return os.path.join(config.Paths().sdk_root, 'bin', 'skaffold')
  return None


def _FindSkaffold():
  """Find the path to the skaffold executable."""
  skaffold = (
      file_utils.FindExecutableOnPath('skaffold') or
      _FindOrInstallSkaffoldComponent())
  if not skaffold:
    raise EnvironmentError('Unable to locate skaffold.')
  return skaffold


@contextlib.contextmanager
def Skaffold(skaffold_config, context_name=None):
  """Run skaffold and catch keyboard interrupts to kill the process.

  Args:
    skaffold_config: Path to skaffold configuration yaml file.
    context_name: Kubernetes context name.

  Yields:
    The skaffold process.
  """
  cmd = [_FindSkaffold(), 'dev', '-f', skaffold_config, '--port-forward']
  if context_name:
    cmd += ['--kube-context', context_name]

  # Supress the current Ctrl-C handler and pass the signal to the child
  # process.
  with _SigInterruptedHandler(_EmptyHandler):
    try:
      p = subprocess.Popen(cmd)
      yield p
    except KeyboardInterrupt:
      p.terminate()
      p.wait()

  sys.stdout.flush()
  sys.stderr.flush()


@base.ReleaseTracks(base.ReleaseTrack.ALPHA)
class Dev(base.Command):
  """Run a service in a development environment.

  By default, this command runs the user's containers on minikube on the local
  machine. To run on another kubernetes cluster, use the --kube-context flag.

  When using minikube, if the minikube cluster is not running, this command
  will start a new minikube cluster with that name.
  """

  @classmethod
  def Args(cls, parser):
    flags.CommonFlags(parser)

    group = parser.add_mutually_exclusive_group(required=False)

    group.add_argument('--kube-context', help='Kubernetes context.')

    group.add_argument('--minikube-profile', help='Minikube profile.')

    group.add_argument('--kind-cluster', help='Kind cluster.')

    parser.add_argument(
        '--delete-cluster',
        default=False,
        action='store_true',
        help='If running on minikube or kind, delete the minkube profile or '
        'kind cluster at the end of the session.')

    parser.add_argument(
        '--minikube-vm-driver',
        default='kvm2',
        help='If running on minikube, use this vm driver.')

  def Run(self, args):
    settings = local.Settings.FromArgs(args)
    local_file_generator = local_files.LocalRuntimeFiles(settings)

    with tempfile.NamedTemporaryFile(mode='w+t') as kubernetes_config:
      with tempfile.NamedTemporaryFile(mode='w+t') as skaffold_config:
        kubernetes_config.write(six.u(local_file_generator.KubernetesConfig()))
        kubernetes_config.flush()
        skaffold_config.write(
            six.u(local_file_generator.SkaffoldConfig(kubernetes_config.name)))
        skaffold_config.flush()

        with self._GetKubernetesEngine(args) as context:
          with Skaffold(skaffold_config.name, context.context_name) as skaffold:
            skaffold.wait()

  @classmethod
  def _GetKubernetesEngine(cls, args):
    """Get the appropriate kubernetes implementation from the args.

    Args:
      args: The namespace containing the args.

    Returns:
      The context manager for the appropriate kubernetes implementation.
    """

    def External():
      return kube_context.ExternalClusterContext(args.kube_context)

    def Kind():
      if args.IsSpecified('kind_cluster'):
        cluster_name = args.kind_cluster
      else:
        cluster_name = DEFAULT_CLUSTER_NAME
      return kube_context.KindClusterContext(cluster_name, args.delete_cluster)

    def Minikube():
      if args.IsSpecified('minikube_profile'):
        cluster_name = args.minikube_profile
      else:
        cluster_name = DEFAULT_CLUSTER_NAME

      return kube_context.Minikube(cluster_name, args.delete_cluster,
                                   args.minikube_vm_driver)

    if args.IsSpecified('kube_context'):
      return External()
    elif args.IsSpecified('kind_cluster'):
      return Kind()
    elif args.IsSpecified('minikube_profile'):
      return Minikube()
    elif platforms.OperatingSystem.Current() == platforms.OperatingSystem.LINUX:
      return Kind()
    else:
      return Minikube()
