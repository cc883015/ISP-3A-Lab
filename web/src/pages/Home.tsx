import { Link } from "react-router-dom";
import { tools } from "../tools/registry";

export function Home() {
  return (
    <div className="page">
      <header className="hero">
        <p className="kicker">ISP-3A-Lab</p>
        <h1>影像实验室 / Imaging lab</h1>
        <p className="lede">
          算法在 <code>python/</code> 和 <code>c/</code> 打磨。这个网页只负责把工具摊开给面试或工作演示。
          <br />
          Algorithms stay in <code>python/</code> and <code>c/</code>. This site only shows the tools.
        </p>
      </header>
      <section className="grid">
        {tools.map((tool) => (
          <article key={tool.id} className="card">
            <div className="card-top">
              <span className={`status status-${tool.status}`}>{tool.status === "live" ? "可演示 / live" : "稍后 / soon"}</span>
              <p className="principles">{tool.principles.join(" · ")}</p>
            </div>
            <h2>
              {tool.titleZh}
              <small>{tool.titleEn}</small>
            </h2>
            <p>{tool.blurbZh}</p>
            <p className="en">{tool.blurbEn}</p>
            {tool.status === "live" ? (
              <Link className="btn" to={tool.path}>
                打开 / Open
              </Link>
            ) : (
              <span className="btn btn-disabled">待接入算法 / wiring later</span>
            )}
          </article>
        ))}
      </section>
    </div>
  );
}
