# nushell-copr
 
Fedora [COPR](https://copr.fedorainfracloud.org) packaging for [Nushell](https://www.nushell.sh). It repackages the official prebuilt upstream release binaries and is kept up to date automatically by GitHub Actions.
 
COPR project: https://copr.fedorainfracloud.org/coprs/cosmicpredator/nushell
 
## Install
 
```bash
sudo dnf copr enable cosmicpredator/nushell
sudo dnf install nushell
```
 
Updates arrive through the normal `dnf upgrade`.
 
Supported architectures: `x86_64` and `aarch64`.
 
## How it works
 
1. A scheduled GitHub Actions workflow runs every 6 hours (and can be triggered manually).
2. It queries the GitHub API for the latest `nushell/nushell` release and compares it to the `Version:` in `nushell.spec`.
3. If upstream is newer, the workflow:
   - bumps the spec file and adds a changelog entry,
   - downloads the release tarballs and builds an SRPM,
   - submits the SRPM to COPR with `copr-cli`,
   - commits the updated spec back to this repo.
4. COPR builds the RPMs for every enabled chroot.
The package does not compile anything. It installs the upstream `nu` binary and any bundled `nu_plugin_*` binaries into `/usr/bin`, and registers `nu` in `/etc/shells`.
 
## Repository layout
 
```
.
├── nushell.spec                 # RPM spec (version is bumped automatically)
└── .github/workflows/update.yml # version check, SRPM build, COPR submit
```
 
## Setting up your own copy
 
1. **COPR account and project**
   - Log in at https://copr.fedorainfracloud.org with a Fedora account.
   - Create the project, enabling the chroots you need and following Fedora branching so new releases are added automatically:
```bash
copr-cli create nushell \
  --chroot fedora-rawhide-x86_64 --chroot fedora-rawhide-aarch64 \
  --chroot fedora-45-x86_64 --chroot fedora-45-aarch64 \
  --chroot fedora-44-x86_64 --chroot fedora-44-aarch64 \
  --follow-fedora-branching on \
  --description "Prebuilt upstream Nushell binaries"
```
 
2. **API token**
   - While logged in, copy the config block from https://copr.fedorainfracloud.org/api/.
   - In your GitHub repo, go to **Settings → Secrets and variables → Actions** and add a secret named `COPR_CONFIG` containing the whole block.
3. **Workflow**
   - Replace `YOUR_COPR_USERNAME` in `.github/workflows/update.yml` with your COPR username (or `@group`).
   - Push to GitHub, then run **Actions → Update Nushell → Run workflow** to trigger the first build.
## Maintenance
 
- **COPR token expiry:** the API token is valid for 180 days. When builds start failing with authentication errors, generate a new token and update the `COPR_CONFIG` secret.
- **Scheduled workflow pause:** GitHub disables scheduled workflows after 60 days without repository activity. The automatic version-bump commits normally prevent this, but if Nushell goes a long time without a release, trigger the workflow manually to re-enable it.
- **Packaging changes:** if upstream changes its tarball layout (for example, adds or removes plugin binaries or the license file), adjust `%install` and `%files` in `nushell.spec`.
- **Old Fedora releases:** COPR removes end-of-life chroots on its own. New releases are enabled automatically if `--follow-fedora-branching` is on.
## Conflicts with the official package
 
Fedora's own repositories may ship a `nushell` package. If both are installed or enabled, they will conflict. Either set the COPR repo priority, or rename this package (for example `nushell-bin` with `Provides: nushell`).
 
## License
 
Nushell is licensed under the MIT License. See the [upstream repository](https://github.com/nushell/nushell) for details. The packaging files in this repository are provided under the same license unless stated otherwise.