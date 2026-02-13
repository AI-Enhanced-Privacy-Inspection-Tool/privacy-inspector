import { useState } from "react";
import { Shield, Sparkles, AlertTriangle } from "lucide-react";
import { Button } from "../components/Button";
import { cn } from "../components/utils";
import { ScanResults } from "./ScanResult";

export function Dashboard() {
  const [activeTab, setActiveTab] = useState<"scan-results" | "ai-insights">("scan-results");

  return (
    <div className="flex flex-col min-h-screen w-full bg-gray-50">
      {/* Header */}
      <header className="w-full bg-white border-b border-gray-200">
        <div className="flex items-center justify-between px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center gap-3">
            <Shield className="w-8 h-8 text-blue-600" />
            <div>
              <h1 className="text-xl font-semibold text-gray-900">Privacy Inspector</h1>
              <p className="text-sm text-gray-500">AI-Enhanced Privacy Analysis</p>
            </div>
          </div>
          <Button>Run New Scan</Button>
        </div>
      </header>


      {/* Text Tabs */}
      <div className="flex gap-8 mt-2 border-b border-slate-200 px-4 sm:px-6 lg:px-8">
        {/* Scan Results Tab */}
        <div
          onClick={() => setActiveTab("scan-results")}
          className={cn(
            "flex items-center gap-2 pb-2 font-semibold cursor-pointer transition-colors border-b-2",
            activeTab === "scan-results"
              ? "border-blue-600 text-blue-600"
              : "border-transparent text-slate-400 hover:text-slate-600"
          )}
        >
          <AlertTriangle className="w-4 h-4" />
          Scan Results
        </div>

        {/* AI Insights Tab */}
        <div
          onClick={() => setActiveTab("ai-insights")}
          className={cn(
            "flex items-center gap-2 pb-2 font-semibold cursor-pointer transition-colors border-b-2",
            activeTab === "ai-insights"
              ? "border-blue-600 text-blue-600"
              : "border-transparent text-slate-400 hover:text-slate-600"
          )}
        >
          <Sparkles className="w-4 h-4" />
          AI Insights
        </div>
      </div>


      {/* Main Content */}
      <main className="flex-1 max-w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {activeTab === "scan-results" ? (
            <ScanResults />
          ) : (
            <div className="flex flex-col items-center justify-center h-64 text-gray-400">
              <Sparkles className="w-12 h-12 mb-4 opacity-20" />
            </div>
        )}
      </main>
    </div>
  );
}
