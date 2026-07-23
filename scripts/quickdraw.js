require("dotenv").config();
const { Octokit } = require("@octokit/rest");

async function main() {
  const token = process.env.GH_PAT || process.env.GITHUB_TOKEN;
  if (!token) {
    throw new Error("No GitHub token found");
  }

  const octokit = new Octokit({ auth: token });
  const owner = "alyamikhailovnaa";
  const repo = "alya";

  console.log("Creating dummy issue for Quickdraw badge...");

  // Create an issue
  const { data: issue } = await octokit.rest.issues.create({
    owner,
    repo,
    title: `Quickdraw Badge Automation - ${new Date().getTime()}`,
    body: "This is an automated issue to achieve the Quickdraw badge.",
  });

  console.log(`Issue created: #${issue.number}`);

  // Wait a few seconds
  await new Promise((resolve) => setTimeout(resolve, 2000));

  // Close the issue
  await octokit.rest.issues.update({
    owner,
    repo,
    issue_number: issue.number,
    state: "closed",
  });

  console.log(`Issue #${issue.number} closed successfully.`);
}

main().catch((err) => {
  console.error("[ERROR] Quickdraw automation failed:", err.message);
  process.exit(1);
});
