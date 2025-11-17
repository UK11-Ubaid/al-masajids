import fetch from "node-fetch";

const OWNER = process.env.GITHUB_OWNER;
const REPO = process.env.GITHUB_REPO;
const BRANCH = process.env.GITHUB_BRANCH;
const TOKEN = process.env.GITHUB_TOKEN;
const API_PASSWORD = process.env.API_PASSWORD;

export default async function handler(req, res) {
  try {
    if (req.method !== "POST") return res.status(405).end();

    if (req.headers["x-api-password"] !== API_PASSWORD)
      return res.status(401).json({ error: "Unauthorized" });

    const { mosque, times } = req.body;
    if (!mosque || !times) return res.status(400).json({ error: "Missing data" });

    const fileUrl = `https://api.github.com/repos/${OWNER}/${REPO}/contents/data/salah_times.json?ref=${BRANCH}`;

    const fileResp = await fetch(fileUrl, {
      headers: { Authorization: `token ${TOKEN}` }
    });
    const fileJson = await fileResp.json();

    const content = Buffer.from(fileJson.content, "base64").toString("utf8");
    const data = JSON.parse(content);

    data[mosque] = times;

    const updatedContent = Buffer.from(JSON.stringify(data, null, 2)).toString("base64");

    const updateResp = await fetch(fileUrl, {
      method: "PUT",
      headers: {
        Authorization: `token ${TOKEN}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        message: `Update ${mosque} times`,
        content: updatedContent,
        branch: BRANCH,
        sha: fileJson.sha
      })
    });

    res.json({ success: true });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
}
