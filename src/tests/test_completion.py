# Copyright (c) 2025 Lunatic Fringers
#
# This file is part of Shepherd Core Stack
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import annotations

from pathlib import Path

import pytest
from click.testing import CliRunner
from pytest_mock import MockerFixture

from shepctl import ShepherdMng

values = """
  # PostgreSQL (pg) Configuration
  pg_image=ghcr.io/lunaticfringers/shepherd/postgres:17-3.5
  pg_empty_env=fresh-pg-1735
  pg_listener_port=5432

  # SHPD Registry Configuration
  shpd_registry=ftp.example.com
  shpd_registry_ftp_usr=
  shpd_registry_ftp_psw=
  shpd_registry_ftp_shpd_path=shpd
  shpd_registry_ftp_imgs_path=imgs

  # Host and Domain Configuration
  host_inet_ip=127.0.0.1
  domain=sslip.io
  dns_type=autoresolving

  # Certificate Authority (CA) Configuration
  ca_country=IT
  ca_state=MS
  ca_locality=Carrara
  ca_org=LunaticFringe
  ca_org_unit=Development
  ca_cn=sslip.io
  ca_email=lf@sslip.io
  ca_passphrase=test

  # Certificate Configuration
  cert_country=IT
  cert_state=MS
  cert_locality=Carrara
  cert_org=LunaticFringe
  cert_org_unit=Development
  cert_cn=sslip.io
  cert_email=lf@sslip.io
  cert_subject_alternative_names=

  shpd_dir=~/shpd

  # Database Default Configuration
  db_sys_usr=sys
  db_sys_psw=sys
  db_usr=docker
  db_psw=docker

  # Logging Configuration
  log_file=~/shpd/shepctl.log
  log_level=WARNING
  log_stdout=false
  log_format=%(asctime)s - %(levelname)s - %(message)s
  """


@pytest.fixture
def temp_home(tmp_path: Path, mocker: MockerFixture) -> Path:
    """Fixture to create a temporary home directory and .shpd.conf file."""
    temp_home = tmp_path / "home"
    temp_home.mkdir()

    config_file = temp_home / ".shpd.conf"
    config_file.write_text(values)

    return temp_home


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


def make_expanduser_side_effect(path: Path, calls: int):
    """Generate a list of `os.path.expanduser` return
    values repeating [shpd, .shpd.conf, shpd/shepctl.log]."""
    return [
        (
            path / ".shpd.conf"
            if i % 3 == 0
            else (
                path / "shpd" if i % 3 == 1 else path / "shpd" / "shepctl.log"
            )
        )
        for i in range(calls * 3)
    ]


@pytest.mark.compl
@pytest.mark.parametrize("expanduser_side_effects", [1])
def test_completion_no_args(
    temp_home: Path,
    runner: CliRunner,
    mocker: MockerFixture,
    expanduser_side_effects: int,
):
    side_effect = make_expanduser_side_effect(
        temp_home, expanduser_side_effects
    )
    mocker.patch("os.path.expanduser", side_effect=side_effect)

    sm = ShepherdMng()
    completions = sm.completionMng.get_completions([])
    assert (
        completions == sm.completionMng.CATEGORIES
    ), "Expected categories only"


@pytest.mark.compl
@pytest.mark.parametrize("expanduser_side_effects", [1])
def test_completion_env_commands(
    temp_home: Path,
    runner: CliRunner,
    mocker: MockerFixture,
    expanduser_side_effects: int,
):
    side_effect = make_expanduser_side_effect(
        temp_home, expanduser_side_effects
    )
    mocker.patch("os.path.expanduser", side_effect=side_effect)

    sm = ShepherdMng()
    completions = sm.completionMng.get_completions(["env"])
    assert (
        completions == sm.completionMng.completionEnvMng.COMMANDS_ENV
    ), "Expected env commands only"


@pytest.mark.compl
@pytest.mark.parametrize("expanduser_side_effects", [1])
def test_completion_db_commands(
    temp_home: Path,
    runner: CliRunner,
    mocker: MockerFixture,
    expanduser_side_effects: int,
):
    side_effect = make_expanduser_side_effect(
        temp_home, expanduser_side_effects
    )
    mocker.patch("os.path.expanduser", side_effect=side_effect)

    sm = ShepherdMng()
    completions = sm.completionMng.get_completions(["db"])
    assert (
        completions == sm.completionMng.completionDbMng.COMMANDS_DB
    ), "Expected db commands only"


@pytest.mark.compl
@pytest.mark.parametrize("expanduser_side_effects", [1])
def test_completion_svc_commands(
    temp_home: Path,
    runner: CliRunner,
    mocker: MockerFixture,
    expanduser_side_effects: int,
):
    side_effect = make_expanduser_side_effect(
        temp_home, expanduser_side_effects
    )
    mocker.patch("os.path.expanduser", side_effect=side_effect)

    sm = ShepherdMng()
    completions = sm.completionMng.get_completions(["svc"])
    assert (
        completions == sm.completionMng.completionSvcMng.COMMANDS_SVC
    ), "Expected svc commands only"
