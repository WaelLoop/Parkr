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
"""Library for generating the files for local development environment."""
from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import os.path
import subprocess
from googlecloudsdk.core import config
from googlecloudsdk.core.updater import update_manager
from googlecloudsdk.core.util import files as file_utils
import six


def _FindOrInstallComponent(component_name):
  """Finds the path to a component or install it.

  Args:
    component_name: Name of the component.

  Returns:
    Path to the component. Returns None if the component can't be found.
  """
  if (config.Paths().sdk_root and
      update_manager.EnsureInstalledAndRestart([component_name])):
    return os.path.join(config.Paths().sdk_root, 'bin', component_name)

  return None


def _FindExecutable(exe):
  """Finds the path to an executable.

  Args:
    exe: Name of the executable.

  Returns:
    Path to the executable.
  Raises:
    EnvironmentError: The exeuctable can't be found.
  """
  path = file_utils.FindExecutableOnPath(exe) or _FindOrInstallComponent(exe)
  if not path:
    raise EnvironmentError('Unable to locate %s.' % exe)
  return path


class KindCluster(object):
  """A cluster on kind.

  Attributes:
    context_name: Kubernetes context name.
  """

  def __init__(self, cluster_name):
    """Initializes KindCluster with cluster name.

    Args:
      cluster_name: Name of cluster.
    """
    self.context_name = 'kind-' + cluster_name


class KindClusterContext(object):
  """Context Manager for running Kind."""

  def __init__(self, cluster_name, delete_cluster=True):
    """Initialize KindContextManager.

    Args:
      cluster_name: Name of the kind cluster.
      delete_cluster: Delete the cluster when the context is exited.
    """
    self._cluster_name = cluster_name
    self._delete_cluster = delete_cluster

  def __enter__(self):
    _StartKindCluster(self._cluster_name)
    return KindCluster(self._cluster_name)

  def __exit__(self, exc_type, exc_value, tb):
    if self._delete_cluster:
      _StopKindCluster(self._cluster_name)


def _StartKindCluster(cluster_name):
  """Starts a kind kubernetes cluster.

  Starts a cluster if a cluster with that name isn't already running.

  Args:
    cluster_name: Name of the kind cluster.
  """
  if not _IsKindClusterUp(cluster_name):
    cmd = [_FindKind(), 'create', 'cluster', '--name', cluster_name]
    subprocess.check_call(cmd)


def _IsKindClusterUp(cluster_name):
  """Checks if a cluster is running.

  Args:
    cluster_name: Name of the cluster

  Returns:
    True if a cluster with the given name is running.
  """
  cmd = [_FindKind(), 'get', 'clusters']
  p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
  stdout, _ = p.communicate()
  lines = six.ensure_text(stdout).strip().splitlines()
  return cluster_name in lines


def _StopKindCluster(cluster_name):
  """Deletes a kind kubernetes cluster.

  Args:
    cluster_name: Name of the cluster.
  """
  cmd = [_FindKind(), 'delete', 'cluster', '--name', cluster_name]
  subprocess.check_call(cmd)


def _FindKind():
  """Finds a path to kind."""
  return _FindExecutable('kind')


class MinikubeCluster(object):
  """A cluster on minikube.

  Attributes:
    context_name: Kubernetes context name.
  """

  def __init__(self, profile):
    """Initializes MinkubeCluster with profile name.

    Args:
      profile: Name of minikube profile.
    """
    self.context_name = profile


class Minikube(object):
  """Starts and stops a minikube cluster."""

  def __init__(self, cluster_name, delete_cluster=True, vm_driver='kvm2'):
    self._cluster_name = cluster_name
    self._delete_cluster = delete_cluster
    self._vm_driver = vm_driver

  def __enter__(self):
    _StartMinkubeCluster(self._cluster_name, self._vm_driver)
    return MinikubeCluster(self._cluster_name)

  def __exit__(self, exc_type, exc_value, tb):
    if self._delete_cluster:
      _DeleteMinikube(self._cluster_name)


def _FindMinikube():
  return _FindExecutable('minikube')


def _StartMinkubeCluster(cluster_name, vm_driver):
  """Starts a minikube cluster."""
  if not _IsMinikubeClusterUp(cluster_name):
    cmd = [
        _FindMinikube(), 'start', '-p', cluster_name, '--keep-context',
        '--vm-driver=' + vm_driver
    ]
    subprocess.check_call(cmd)


def _IsMinikubeClusterUp(cluster_name):
  """Checks if a minikube cluster is running."""
  cmd = [_FindMinikube(), 'status', '-p', cluster_name]
  p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
  stdout, _ = p.communicate()
  lines = six.ensure_text(stdout).strip().splitlines()
  status = dict(line.split(':', 1) for line in lines)
  return 'host' in status and status['host'].strip() == 'Running'


def _DeleteMinikube(cluster_name):
  """Delete a minikube cluster."""
  cmd = [_FindMinikube(), 'delete', '-p', cluster_name]
  subprocess.check_call(cmd)


class ExternalCluster(object):
  """A external kubernetes cluster.

  Attributes:
    context_name: Kubernetes context name.
  """

  def __init__(self, cluster_name):
    """Initializes ExternalCluster with profile name.

    Args:
      cluster_name: Name of the cluster.
    """
    self.context_name = cluster_name


class ExternalClusterContext(object):
  """Do nothing context manager for external clusters."""

  def __init__(self, kube_context):
    self._kube_context = kube_context

  def __enter__(self):
    return ExternalCluster(self._kube_context)

  def __exit__(self, exc_type, exc_value, tb):
    pass
