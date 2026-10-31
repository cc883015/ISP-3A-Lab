import { Link, Navigate, Route, Routes } from "react-router-dom";
import { Home } from "./pages/Home";
import { IqLab } from "./pages/IqLab";

export function App() {
  return (
    <div className="shell">
      <nav className="nav">
        <Link className="brand" to="/">
          ISP-3A-Lab
        </Link>
        <span>展示站 / showcase</span>
      </nav>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/tools/iq-lab" element={<IqLab />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </div>
  );
}
