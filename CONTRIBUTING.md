# Be a 420Tech Compassion Ambassador
🥦 Thank you for offering your labor toward expanding access to plant medicine! 🥦
## Submitting Issues
Write a draft story in the [Backlog](https://github.com/orgs/ReCompass/projects/5/views/1) & TODO: comms.
## Style Guide
On our [Drive](https://docs.google.com/document/d/1wPZ0LF5d_gib5UaMepqtHy-5TprYIEwgk9-98xkvjVM/edit#heading=h.v65wzw63m1gb) so it can change a lot with us.
## Submitting Changes
1. Put up a PR and fill in the description headers that make sense.
2. Get a review.
3. Merge to `main` and delete your remote dev branch.
## Onboarding to the Repo as a Developer
All of this should be run from the project root. These steps wil create a bash profile and source your terminal with it at the end.
### Requirements
- View rights on (TODO: Service Acct)
### (PC Users) Install Git Bash and establish a .bashrc
TODO: Do we need this section?
#### Install Git Bash
1. Install from https://gitforwindows.org/
2. Open Git Bash
#### Establish a .bashrc
```bash
touch ~/.bashrc
```
All commands below that call for ~/.zshrc, use ~/.bashrc
### Conda Environment
We use Miniconda, a minimal import of Anaconda, to manage environments. It's available on most operating systems.
#### Install
1. Attempt to install the latest using their [high level commands](https://docs.conda.io/projects/miniconda/en/latest/index.html#quick-command-line-install)
2. If necessary, follow instructions on the linked page for dialing to your system requirements.
#### Create the Environment
Installing conda also installs pip, so you can run:
```bash
conda create -n sb34rag python=$(cat .python-version)
conda activate sb34rag
pip install -r requirements.txt
```
### Python Path
This will extend your PYTHONPATH. If you don't have one set, you can remove the `:$PYTHONPATH`.
```bash
echo 'export PYTHONPATH=/path/to/sb34rag:$PYTHONPATH' >> ~/.zshrc
```
### Set Pre-Commit Hooks
```bash
pre-commit install
```
### Source changes to your terminal from your .zshrc
```bash
source ~/.zshrc
```
### Set Service Account Credentials
TODO
### Test you're set up properly
#### Echo Environment Variable(s)
```bash
echo $PYTHONPATH
```
#### Run Tests
```bash
pytest
```
#### Run Application
 TODO
## Onboarding to the Repo as DevOps: Establish Connection to GCP
### Requirements
Must have an account in the ReCompass Google Workspace. Don't know the proper scoping of permissions and not sure if I'll ever have to solve that. Still good to keep some notes here.
### Init `gcloud` CLI
[Download from Google](https://cloud.google.com/sdk/docs/install)
### Point the SDK to your environment's Python
CloudSDK automatically points to your system's base python, but requires python>=3.7.
```bash
echo 'export CLOUDSDK_PYTHON=$(which python)' >> ~/.zshrc
```
### Set your default project
TODO
### Test you're set up properly
#### Echo Environment Variable(s)
```bash
echo $CLOUDSDK_PYTHON
```
#### Deploy test app
TODO
