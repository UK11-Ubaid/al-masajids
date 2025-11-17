const OWNER = process.env.GITHUB_OWNER;
const REPO = process.env.GITHUB_REPO;
const BRANCH = process.env.GITHUB_BRANCH;
const TOKEN = process.env.GITHUB_TOKEN;

export default async function handler(req, res) {
  try {
    const mosque = req.query.mosque;
    if (!mosque) return res.status(400).json({ error: "mosque required" });

    const url = `https://api.github.com/repos/${OWNER}/${REPO}/contents/data/salah_times.json?ref=${BRANCH}`;

    const resp = await fetch(url, {
      headers: { Authorization: `token ${TOKEN}` }
    });
    const json = await resp.json();

    const content = Buffer.from(json.content, "base64").toString("utf8");
    const data = JSON.parse(content);

    res.json(data[mosque] || {});
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
}
