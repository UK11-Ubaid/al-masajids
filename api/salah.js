import fs from "fs";
import path from "path";

export default function handler(req, res) {
    const mosque = req.query.mosque;
    if (!mosque) return res.status(400).json({ error: "Mosque is required" });

    const filePath = path.join(process.cwd(), "../data/salah_times.json");
    const data = JSON.parse(fs.readFileSync(filePath, "utf8"));

    if (!data[mosque]) {
        return res.status(404).json({ error: "Mosque not found" });
    }

    res.status(200).json({ [mosque]: data[mosque] });
}
