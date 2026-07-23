require('dotenv').config();
const { Octokit } = require('@octokit/rest');

async function main() {
  const token = process.env.GH_PAT || process.env.GITHUB_TOKEN;
  if (!token) {
    throw new Error('No GitHub token found');
  }

  const octokit = new Octokit({ auth: token });
  const owner = 'alyamikhailovnaa';
  const repo = 'alya';
  const branchName = `yolo-${new Date().getTime()}`;

  console.log('Fetching repository details...');
  
  // 1. Get default branch reference
  const { data: repoData } = await octokit.rest.repos.get({ owner, repo });
  const defaultBranch = repoData.default_branch;

  const { data: refData } = await octokit.rest.git.getRef({
    owner,
    repo,
    ref: `heads/${defaultBranch}`,
  });
  const sha = refData.object.sha;

  // 2. Create new branch
  console.log(`Creating branch ${branchName}...`);
  await octokit.rest.git.createRef({
    owner,
    repo,
    ref: `refs/heads/${branchName}`,
    sha,
  });

  // 3. Create or update a file in the new branch
  const filePath = `logs/yolo-dummy.md`;
  const fileContent = Buffer.from(`YOLO commit at ${new Date().toISOString()}`).toString('base64');
  
  let fileSha;
  try {
    const { data: existingFile } = await octokit.rest.repos.getContent({
      owner,
      repo,
      path: filePath,
      ref: branchName
    });
    fileSha = existingFile.sha;
  } catch (err) {
    // File doesn't exist, which is fine
  }

  console.log('Committing file...');
  await octokit.rest.repos.createOrUpdateFileContents({
    owner,
    repo,
    path: filePath,
    message: 'YOLO automated commit',
    content: fileContent,
    branch: branchName,
    sha: fileSha
  });

  // 4. Create Pull Request
  console.log('Creating Pull Request...');
  const { data: pr } = await octokit.rest.pulls.create({
    owner,
    repo,
    title: `YOLO Badge Automation - ${branchName}`,
    head: branchName,
    base: defaultBranch,
    body: 'Automated PR to trigger YOLO badge.'
  });

  console.log(`Pull Request created: #${pr.number}`);

  // 5. Merge Pull Request
  console.log('Merging Pull Request...');
  await octokit.rest.pulls.merge({
    owner,
    repo,
    pull_number: pr.number,
    merge_method: 'squash'
  });

  console.log(`Pull Request #${pr.number} merged successfully! YOLO achieved.`);
  
  // 6. Delete branch
  console.log('Cleaning up branch...');
  await octokit.rest.git.deleteRef({
    owner,
    repo,
    ref: `heads/${branchName}`
  });
  
  console.log('Branch cleaned up.');
}

main().catch(err => {
  console.error('[ERROR] YOLO automation failed:', err.message);
  process.exit(1);
});
