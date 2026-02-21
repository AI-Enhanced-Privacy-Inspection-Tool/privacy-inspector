import { ShieldCheck, AlertCircle, Cookie, Fingerprint, Database, FolderOpen, Play, Sparkles, ChevronDown } from "lucide-react";
import { RiskBadge } from "../components/RiskBadge";
import { Card, CardContent } from "../components/Card";
import { Button } from "../components/Button";
import LoadingScan from "../components/LoadingScan";
import { useState } from "react";
import { LocalAiInsight } from "../components/LocalAiInsight";

export function ScanResults() {
  const [isScanning, setIsScanning] = useState(false);
  const [expandedInsight, setExpandedInsight] = useState<string | null>(null);
  const [scanResults, setScanResults] = useState<any>(null); 

  const handleStartScan = async () => {
    setIsScanning(true); 

    try {
      const response = await fetch("http://localhost:8000/scan/desktop", {
        method: "POST",
      });
      const data = await response.json();
      setScanResults(data); 
    } catch (error) {
      console.error("Error running scan:", error);
    } finally {
      console.log("Scan completed or failed. Results:", scanResults);
      setIsScanning(false); 
    }
  };

  const toggleInsight = (id: string) => {
    setExpandedInsight(expandedInsight === id ? null : id);
  };

  if (isScanning) {
    return <LoadingScan onStop={() => setIsScanning(false)} />;
  }

  return (
    <div className="w-full max-w-6xl mx-auto px-6 space-y-8 animate-in fade-in duration-500">  
      {/* Header */}
      <div className="space-y-6">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">
            Privacy Scan Results
          </h2>
          <p className="text-gray-500">
            Summary of privacy issues detected in your system
          </p>
        </div>

        {/* Privacy Scan Card */}
        <div className="bg-[#f5f8ff] border border-[#e2e8f0] rounded-2xl p-8">
          <div className="flex flex-col gap-4">
            {/* Icon and Title */}
            <div className="flex items-center gap-3">
              <FolderOpen className="w-6 h-6 text-gray-800" strokeWidth={2.5} />
              <h3 className="text-lg font-bold text-gray-900">
                Start Local Privacy Scan
              </h3>
            </div>

            {/* Description */}
            <p className="text-gray-500 text-lg">
              Scan your local system for cookies, browser data, and application privacy risks
            </p>

            {/* Action Button */}
            <div className="mt-2">
              <Button size="lg" 
                icon={Play}
                onClick={handleStartScan} 
                className="bg-[#1a68ff] hover:bg-[#0052cc] rounded-lg px-8 font-semibold">
                Run Scan
              </Button>
            </div>

            {/* Note Section */}
            <div className="mt-4 bg-white/60 rounded-xl p-4 border border-white/40">
              <p className="text-sm text-gray-600">
                <span className="font-bold text-gray-800">Note:</span> The scan will analyze browser cookies, local storage, session data, and application data for privacy risks. This process may take a few moments.
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Last Scan Summary */}
      <Card className="bg-blue-50 border-blue-100 shadow-sm">
        <CardContent className="pt-6 flex items-start gap-4">
          <div className="bg-blue-600 p-3 rounded-xl">
            <ShieldCheck className="w-6 h-6 text-white" />
          </div>

          <div className="flex-1">
            <h3 className="font-bold text-gray-900 text-lg">
              Last Scan Completed
            </h3>

            <p className="text-blue-600/70 text-sm flex items-center gap-1">
              <span className="opacity-70">🕒</span>
              {new Date().toLocaleString()} 
            </p>

            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-6">
              {[
                { label: "Cookies", value: scanResults.cookies?.length || 0 },
                { label: "Identifiers", value: scanResults.identifiers?.length || 0 },
                { label: "Apps Scanned", value: scanResults.apps?.length || 0 },
                { label: "Total Data", value: scanResults.totalSize || "0 MB" },
              ].map((stat) => (
                <Card key={stat.label} className="shadow-none">
                  <CardContent className="pt-4 pb-4">
                    <p className="text-gray-500 text-xs font-medium uppercase">
                      {stat.label}
                    </p>
                    <p className="text-xl font-bold text-gray-900">
                      {stat.value}
                    </p>
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Critical Alert */}
      {scanResults && scanResults.highRiskCount > 0 && (
      <Card className="bg-red-50 border-red-100 shadow-sm">
        <CardContent className="pt-6 flex items-center gap-4">
          <div className="bg-white rounded-full p-1 border border-red-200">
            <AlertCircle className="w-6 h-6 text-red-600" />
          </div>

          <div>
            <p className="text-red-900 font-bold">
              {scanResults.highRiskCount} Privacy Issues Detected
            </p>
            <p className="text-red-700 text-sm font-medium">
              High and critical risk items requiring attention
            </p>
          </div>
        </CardContent>
      </Card>
      )}

      {/* Summary Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {[
          {
            label: "Tracking Cookies",
            value: scanResults.cookies?.length || 0,
            desc: "High-risk cookies found",
            icon: <Cookie className="w-5 h-5 text-red-600" />,
          },
          {
            label: "Identifiers",
            value: scanResults.identifiers?.length || 0,
            desc: "Persistent tracking identifiers",
            icon: <Fingerprint className="w-5 h-5 text-red-600" />,
          },
          {
            label: "App Data",
            value: scanResults.apps?.length || 0,
            desc: "Apps with privacy concerns",
            icon: <FolderOpen className="w-5 h-5 text-red-600" />,
          },
        ].map((stat) => (
          <Card key={stat.label} className="shadow-sm">
            <CardContent className="pt-6">
              <div className="flex items-center gap-2 mb-6">
                {stat.icon}
                <span className="text-gray-900 font-semibold text-sm">
                  {stat.label}
                </span>
              </div>

              <p className="text-3xl font-bold text-red-600">
                {stat.value}
              </p>

              <p className="text-xs text-gray-400 font-medium mt-1">
                {stat.desc}
              </p>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* High-Risk Cookies */}
      {scanResults?.cookies?.length > 0 && (
      <section className="space-y-4">
        <div className="flex items-center gap-2">
          <Cookie className="w-6 h-6 text-red-600" />
          <h3 className="text-xl font-bold text-gray-900">
            High-Risk Cookies
          </h3>
        </div>

        {scanResults.cookies.map((cookie: any, idx: number) => (
        <Card key={idx} className="border-[#ffe4d6] bg-white rounded-2xl overflow-hidden shadow-sm">
          <CardContent className="p-6">
            {/* Header */}
            <div className="flex items-center gap-3 mb-4">
              <span className="text-lg font-bold text-gray-900">
                {cookie.name}
              </span>
              <RiskBadge variant="high" className="bg-[#fff1e7] text-[#d97706] border-none font-bold">
                High Risk
              </RiskBadge>
            </div>

            {/* Information */}
            <div className="space-y-2 text-sm text-gray-600 mb-6">
              <p>
                <span className="font-medium text-gray-400">Domain:</span> 
                <span className="ml-2 font-medium text-gray-700">{cookie.domain}</span>
              </p>
              <p>
                <span className="font-medium text-gray-400">Category:</span> 
                <span className="ml-2 font-medium text-gray-700">{cookie.category}</span>
              </p>
              <p>
                <span className="font-medium text-gray-400">Path:</span> 
                <span className="ml-2 font-mono text-gray-700">{cookie.path}</span>
              </p>
              <p>
                <span className="font-medium text-gray-400">Expires:</span> 
                <span className="ml-2 font-medium text-gray-700">{cookie.expires}</span>
              </p>
            </div>

            {/* AI Privacy Insight */}
            <div className="mt-4 pt-4 border-t border-gray-100">
              <button onClick={() => toggleInsight('cookie-1')} className="flex items-center justify-between w-full px-4 py-3 bg-[#fafafa] rounded-xl border border-gray-100 group">
                <div className="flex items-center gap-2 text-[#8b5cf6] font-semibold text-sm">
                  <Sparkles className="size-4 fill-current" /> AI Privacy Insight
                </div>
                <ChevronDown className={`size-4 text-gray-400 transition-transform ${expandedInsight === 'cookie-1' ? 'rotate-180' : ''}`} />
              </button>
              {expandedInsight === 'cookie-1' && <LocalAiInsight type="cookie" />}
            </div>
          </CardContent>
        </Card>
        ))}
      </section>
      )}

      {/* Persistent Identifiers */}
      {scanResults?.identifiers?.length > 0 && (
      <section className="space-y-4">
        <div className="flex items-center gap-2">
          <Fingerprint className="w-6 h-6 text-red-600" />
          <h3 className="text-xl font-bold text-gray-900">
            Persistent Identifiers
          </h3>
        </div>

        {scanResults.identifiers.map((id: any, idx: number) => (
        <Card key={idx} className="border-[#ffe4d6] bg-white rounded-2xl overflow-hidden shadow-sm">
          <CardContent className="p-6">
            <div className="flex items-center gap-3 mb-4">
              <span className="text-lg font-bold text-gray-900">{id.name}</span>
              <RiskBadge variant="critical" className="bg-red-50 text-red-600 border-none font-bold">
                Critical Risk
              </RiskBadge>
            </div>

            <div className="space-y-2 text-sm text-gray-600 mb-6">
              <p>
                <span className="font-medium text-gray-400">Description:</span> 
                <span className="ml-2 font-medium text-gray-700">{id.description}</span>
              </p>
              <p>
                <span className="font-medium text-gray-400">Path:</span> 
                <span className="ml-2 font-mono text-gray-700">{id.path}</span>
              </p>
              <p>
                <span className="font-medium text-gray-400">Value:</span> 
                <span className="ml-2 font-mono text-gray-700">{id.value}</span>
              </p>
              <p>
                <span className="font-medium text-gray-400">Last Seen:</span> 
                <span className="ml-2 font-medium text-gray-700">{id.lastSeen}</span>
              </p>
            </div>

            {/* AI Privacy Insight */}
            <div className="mt-4 pt-4 border-t border-gray-100">
              <button 
                onClick={() => toggleInsight('id-1')} 
                className="flex items-center justify-between w-full px-4 py-3 bg-[#fafafa] rounded-xl border border-gray-100 group">
                <div className="flex items-center gap-2 text-[#8b5cf6] font-semibold text-sm">
                  <Sparkles className="size-4 fill-current" /> AI Privacy Insight
                </div>
                <ChevronDown className={`size-4 text-gray-400 transition-transform ${expandedInsight === 'id-1' ? 'rotate-180' : ''}`} />
              </button>
              {expandedInsight === 'id-1' && <LocalAiInsight type="identifier" />}
            </div>
          </CardContent>
        </Card>
        ))}
      </section>
      )}

      {/* Applications */}
      {scanResults?.apps?.length > 0 && (
      <section className="space-y-4">
        <div className="flex items-center gap-2">
          <Database className="w-6 h-6 text-red-600" />
          <h3 className="text-xl font-bold text-gray-900">
            Applications with Privacy Concerns
          </h3>
        </div>

        {scanResults.apps.map((app: any, idx: number) => (
        <Card key={idx} className="border-[#ffe4d6] bg-white rounded-2xl overflow-hidden shadow-sm">
          <CardContent className="p-6">
            <div className="flex items-center gap-3 mb-4">
              <span className="text-lg font-bold text-gray-900">{app.name}</span>
              <RiskBadge variant="high" className="bg-[#fff1e7] text-[#d97706] border-none font-bold">
                High Risk
              </RiskBadge>
            </div>

            <div className="space-y-2 text-sm text-gray-600 mb-6">
              <p>
                <span className="font-medium text-gray-400">Path:</span> 
                <span className="ml-2 font-mono text-gray-700">{app.path}</span>
              </p>
              <p>
                <span className="font-medium text-gray-400">Category:</span> 
                <span className="ml-2 font-medium text-gray-700">{app.category}</span>
              </p>
              <p>
                <span className="font-medium text-gray-400">Total Size:</span> 
                <span className="ml-2 font-medium text-gray-700">{app.size}</span>
              </p>
            </div>

            {/* AI Privacy Insight */}
            <div className="mt-4 pt-4 border-t border-gray-100">
              <button onClick={() => toggleInsight('app-1')} className="flex items-center justify-between w-full px-4 py-3 bg-[#fafafa] rounded-xl border border-gray-100 group">
                <div className="flex items-center gap-2 text-[#8b5cf6] font-semibold text-sm">
                  <Sparkles className="size-4 fill-current" /> AI Privacy Insight
                </div>
                <ChevronDown className={`size-4 text-gray-400 transition-transform ${expandedInsight === 'app-1' ? 'rotate-180' : ''}`} />
              </button>
              {expandedInsight === 'app-1' && <LocalAiInsight type="app" />}
            </div>
          </CardContent>
        </Card>
        ))}
      </section>
      )}
    </div>
  );
}
