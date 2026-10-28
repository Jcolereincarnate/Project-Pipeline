import { useEffect, useState } from "react";

const API = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000/api";

export default function App() {
  const [jobs, setJobs] = useState([]);
  const [runs, setRuns] = useState([]);
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  async function loadData() {
    try {
      const [jobsRes, runsRes] = await Promise.all([
        fetch(`${API}/jobs/?q=${encodeURIComponent(query)}`),
        fetch(`${API}/pipeline/runs/`),
      ]);
      if (!jobsRes.ok || !runsRes.ok) throw new Error("API request failed. Is Django running?");
      const [jobsData, runsData] = await Promise.all([jobsRes.json(), runsRes.json()]);
      setJobs(jobsData.results || jobsData);
      setRuns(runsData.results || runsData);
      setMessage("");
    } catch (err) { setMessage(err.message); }
  }

  useEffect(() => { loadData(); }, [query]);

  async function runPipeline() {
    setLoading(true); setMessage("Starting pipeline…");
    try {
      const response = await fetch(`${API}/pipeline/run/`, {
        method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ mode: "sync" }),
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.error_message || data.detail || "Pipeline failed. Check the run history.");
      setMessage(`Run ${data.id}: ${data.status}. Saved ${data.jobs_saved} new jobs.`);
      await loadData();
    } catch (err) { setMessage(err.message); }
    finally { setLoading(false); }
  }

  async function updateStatus(job, application_status) {
    const response = await fetch(`${API}/jobs/${job.id}/`, {
      method: "PATCH", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ application_status }),
    });
    if (response.ok) loadData();
    else setMessage("Could not update application status.");
  }

  return <main className="shell">
    <header className="topbar">
      <div><p className="eyebrow">PERSONAL JOB DISCOVERY</p><h1>Job Pipeline</h1><p className="muted">Reddit opportunities, in one place.</p></div>
      <button className="primary" onClick={runPipeline} disabled={loading}>{loading ? "Running…" : "▶ Run pipeline"}</button>
    </header>
    {message && <div className="notice" role="status">{message}</div>}
    <section className="stats">
      <article className="stat"><span>Discovered jobs</span><strong>{jobs.length}</strong></article>
      <article className="stat"><span>Pipeline runs</span><strong>{runs.length}</strong></article>
      <article className="stat"><span>Source</span><strong>Reddit</strong></article>
    </section>
    <section className="panel">
      <div className="section-heading"><div><h2>Job matches</h2><p className="muted">Junior and mid-level · Remote worldwide + Nigeria</p></div>
        <input aria-label="Search jobs" placeholder="Search titles and descriptions…" value={query} onChange={e => setQuery(e.target.value)} />
      </div>
      {jobs.length === 0 ? <div className="empty"><h3>No jobs yet</h3><p>Run the pipeline after configuring approved Reddit API access. Existing matches will appear here.</p></div> :
        <div className="job-list">{jobs.map(job => <article className="job" key={job.id}>
          <div className="job-main"><div className="job-title-row"><h3>{job.title}</h3><span className="score">{job.relevance_score}% match</span></div>
            <p className="muted">{job.company || "Company not identified"} · r/{job.subreddit || "reddit"} · {job.remote ? "Remote" : (job.location_label || "Location unspecified")}</p>
            <p className="description">{(job.description || "No description available.").slice(0, 320)}</p>
            <div className="tags">{(job.matched_tags || []).map(tag => <span key={tag}>{tag}</span>)}</div>
          </div>
          <div className="job-actions"><select aria-label={`Application status for ${job.title}`} value={job.application_status} onChange={e => updateStatus(job, e.target.value)}>
            {["new","saved","interested","applied","interviewing","rejected","offer"].map(s => <option key={s} value={s}>{s[0].toUpperCase()+s.slice(1)}</option>)}
          </select><a href={job.source_url} target="_blank" rel="noreferrer">Open post ↗</a></div>
        </article>)}</div>}
    </section>
    <section className="panel"><div className="section-heading"><div><h2>Recent pipeline runs</h2><p className="muted">Collection history and diagnostics</p></div></div>
      {runs.length === 0 ? <p className="muted">No runs recorded yet.</p> : <div className="run-list">{runs.slice(0, 8).map(run => <div className="run" key={run.id}>
        <div><strong>Run #{run.id}</strong><p className="muted">{new Date(run.started_at).toLocaleString()} · {run.trigger}</p></div>
        <span className={`status ${run.status}`}>{run.status}</span><span>{run.jobs_saved} saved</span>
        {run.error_message && <p className="error">{run.error_message}</p>}
      </div>)}</div>}
    </section>
    <footer>Built with React + Django REST Framework · Reddit API access required for live collection</footer>
  </main>;
}
