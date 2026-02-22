import { ShieldCheck, AlertCircle, Fingerprint, Database, FolderOpen, Play, Sparkles, ChevronDown } from "lucide-react";
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

      console.log("Scan results:", data);
      setScanResults(data);
    } catch (error) {
      console.error("Error running scan:", error);
    } finally {
      setIsScanning(false);
    }
  };

  // Helper function to get stats
  const getStats = () => {
    if (!scanResults) return { totalItems: 0, piiCount: 0, trackingCount: 0, highRiskCount: 0, appCount: 0 };

    const summary = scanResults.summary || {};
    const apps = summary.scanner?.formatted_results?.apps || {};

    return {
      totalItems: summary.total_items || 0,
      piiCount: summary.pii_count || 0,
      trackingCount: summary.tracking_count || 0,
      highRiskCount: summary.high_risk_count || 0,
      appCount: Object.keys(apps).length
    };
  };

  const stats = getStats();

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
                <span className="font-bold text-gray-800">Note:</span> The scan will analyze browser cookies, local storage, session data, and application data for privacy risks. This process typically takes 10-20 minutes depending on the amount of data stored on your system.
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
                { label: "Total Items", value: stats.totalItems },
                { label: "PII Found", value: stats.piiCount },
                { label: "Tracking Items", value: stats.trackingCount },
                { label: "Apps Scanned", value: stats.appCount },
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
      {scanResults && stats.highRiskCount > 0 && (
        <Card className="bg-red-50 border-red-100 shadow-sm">
          <CardContent className="pt-6 flex items-center gap-4">
            <div className="bg-white rounded-full p-1 border border-red-200">
              <AlertCircle className="w-6 h-6 text-red-600" />
            </div>

            <div>
              <p className="text-red-900 font-bold">
                {stats.highRiskCount} High Risk Privacy Issues Detected
              </p>
              <p className="text-red-700 text-sm font-medium">
                Critical items requiring immediate attention
              </p>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Privacy Issues Alert */}
      {scanResults && stats.totalItems > 0 && (
        <Card className="bg-red-50 border-red-200 shadow-sm">
          <CardContent className="pt-6 pb-6">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-4">
                <div className="bg-red-100 rounded-full p-3">
                  <AlertCircle className="w-6 h-6 text-red-600" />
                </div>
                <div>
                  <p className="text-red-900 font-bold text-lg">
                    {stats.totalItems} Privacy Issues Detected
                  </p>
                  <p className="text-red-700 text-sm font-medium">
                    High and critical risk items requiring attention
                  </p>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      )}
      )}

      {/* Summary Metrics */}
      {scanResults && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {[
            {
              label: "PII Found",
              value: stats.piiCount,
              desc: "Personal information detected",
              icon: <Database className="w-5 h-5 text-red-600" />,
            },
            {
              label: "Tracking Items",
              value: stats.trackingCount,
              desc: "Tracking data found",
              icon: <Fingerprint className="w-5 h-5 text-orange-600" />,
            },
            {
              label: "Applications",
              value: stats.appCount,
              desc: "Apps with privacy data",
              icon: <FolderOpen className="w-5 h-5 text-blue-600" />,
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

                <p className="text-3xl font-bold text-gray-900">
                  {stat.value}
                </p>

                <p className="text-xs text-gray-400 font-medium mt-1">
                  {stat.desc}
                </p>
              </CardContent>
            </Card>
          ))}
        </div>
      )}

      {/* AI Analyzed Items */}
      {scanResults?.analyzed_items && scanResults.analyzed_items.length > 0 && (
        <section className="space-y-4">
          <div>
            <div className="flex items-center gap-2 mb-2">
              <Sparkles className="w-6 h-6 text-purple-600" />
              <h3 className="text-xl font-bold text-gray-900">
                Privacy Scan Results
              </h3>
            </div>
            <p className="text-gray-500 text-sm ml-8">
              Detailed analysis of privacy data found on your system
            </p>
          </div>

          {scanResults.analyzed_items.map((item: any, idx: number) => (
            <Card key={idx} className="border-gray-200 bg-white rounded-2xl overflow-hidden shadow-sm">
              <CardContent className="p-6">
                {/* Header */}
                <div className="flex items-center justify-between gap-3 mb-2">
                  <div className="flex items-center gap-3">
                    <span className="text-lg font-bold text-gray-900">
                      {item.name.split(':')[1] || item.name}
                    </span>
                    <RiskBadge variant={item.risk_assessment?.risk_level || 'low'} className={`
                  ${item.risk_assessment?.risk_level === 'high' ? 'bg-red-50 text-red-600' : ''}
                  ${item.risk_assessment?.risk_level === 'medium' ? 'bg-orange-50 text-orange-600' : ''}
                  ${item.risk_assessment?.risk_level === 'low' ? 'bg-green-50 text-green-600' : ''}
                  border-none font-bold capitalize
                `}>
                      {item.risk_assessment?.risk_level || 'low'} Risk
                    </RiskBadge>
                  </div>
                </div>

                {/* App Name */}
                <p className="text-sm font-semibold text-gray-600 mb-4">
                  Application: <span className="text-gray-900">{item.domain}</span>
                </p>

                {/* Value Preview */}
                <div className="mb-4 p-3 bg-gray-50 rounded-lg">
                  <p className="text-xs font-medium text-gray-400 mb-1">Value Preview</p>
                  <p className="text-sm font-mono text-gray-700 truncate">{item.value}</p>
                </div>

                {/* Information */}
                <div className="space-y-2 text-sm text-gray-600 mb-6">
                  {item.metadata && (
                    <>
                      <p>
                        <span className="font-medium text-gray-400">Category:</span>
                        <span className="ml-2 font-medium text-gray-700">{item.metadata.category}</span>
                      </p>
                      <p>
                        <span className="font-medium text-gray-400">Detection Method:</span>
                        <span className="ml-2 font-medium text-gray-700">{item.metadata.detection_method}</span>
                      </p>
                      <p>
                        <span className="font-medium text-gray-400">Confidence:</span>
                        <span className="ml-2 font-medium text-gray-700 capitalize">{item.metadata.confidence}</span>
                      </p>
                    </>
                  )}
                </div>

                {/* AI Privacy Insight */}
                <div className="mt-4 pt-4 border-t border-gray-100">
                  <button onClick={() => toggleInsight(`item-${idx}`)} className="flex items-center justify-between w-full px-4 py-3 bg-[#fafafa] rounded-xl border border-gray-100 group hover:bg-purple-50 transition-colors">
                    <div className="flex items-center gap-2 text-[#8b5cf6] font-semibold text-sm">
                      <Sparkles className="size-4 fill-current" /> AI Privacy Insight
                    </div>
                    <ChevronDown className={`size-4 text-gray-400 transition-transform ${expandedInsight === `item-${idx}` ? 'rotate-180' : ''}`} />
                  </button>
                  {expandedInsight === `item-${idx}` && <LocalAiInsight item={item} />}
                </div>
              </CardContent>
            </Card>
          ))}
        </section>
      )}
      )}

      {/* Recommendations */}
      {scanResults?.recommendations && scanResults.recommendations.length > 0 && (
        <section className="space-y-4">
          <div className="flex items-center gap-2">
            <ShieldCheck className="w-6 h-6 text-blue-600" />
            <h3 className="text-xl font-bold text-gray-900">
              AI Recommendations
            </h3>
          </div>

          <Card className="border-blue-200 bg-blue-50 rounded-2xl">
            <CardContent className="p-6">
              <ul className="space-y-3">
                {scanResults.recommendations.map((rec: string, idx: number) => (
                  <li key={idx} className="flex items-start gap-3 text-sm text-blue-900">
                    <span className="mt-1.5 size-2 rounded-full bg-blue-600 shrink-0" />
                    <span>{rec}</span>
                  </li>
                ))}
              </ul>
            </CardContent>
          </Card>
        </section>
      )}
      )}
    </div>
  );
}
