import ClerkProviderWithRoutes from "./auth/ClerkProviderWithRoutes.jsx";
import { Routes, Route } from "react-router-dom";
import { Layout } from "./layout/Layout.jsx";
import { ChallengeGenerator } from "./challenge/ChallengeGenerator.jsx";
import { HistoryPanel } from "./history/HIstoryPanel.jsx";
import { AuthenticationPage } from "./auth/AuthenticationPage.jsx";
import './App.css'

function App() {
  return <ClerkProviderWithRoutes>
    <Routes>
      {/* the * means a pattern match so if we have anypage that starts with sign in we want to go to the sign in page */}
      <Route path="/sign-in/*" element={<AuthenticationPage />} />
      <Route path="/sign-up" element={<AuthenticationPage />} />
      {/* All the other pages just show up inside that layout */}
      <Route element={<Layout />}>
        <Route path="/" element={<ChallengeGenerator />} />
        <Route path="/history" element={<HistoryPanel />} />
      </Route>
    </Routes>
  </ClerkProviderWithRoutes>
}

export default App
