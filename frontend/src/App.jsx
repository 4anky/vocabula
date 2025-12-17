import "react"
import { useState }

export default function App() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  async function callBackend() {
    setLoading(true);
    setResult(null);
    try {
      const res = await fetch("/api", { method: "GET" });
      const text = await res.text();
      setResult({ ok: res.ok, text });
    } catch (err) {
      setResult({ ok: false, text: err.message });
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={{
      height: "100vh",
      display: "grid",
      placeItems: "center",
      background: "white"
    }}>
      <div style={{ textAlign: "center" }}>
        <button onClick={callBackend} disabled={loading} style={{padding: "10px 18px", fontSize: 16}}>
          {loading ? "Calling..." : "Check backend"}
        </button>

        {result && (
          <div style={{ marginTop: 12, fontFamily: "monospace" }}>
            <div><strong>ok:</strong> {String(result.ok)}</div>
            <div><strong>response:</strong> {result.text}</div>
          </div>
        )}
      </div>
    </div>
  );
}
