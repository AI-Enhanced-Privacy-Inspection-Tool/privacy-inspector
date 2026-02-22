import { Globe, ShieldAlert, Search, Play, Sparkles, ChevronDown, AlertTriangle, CheckCircle2, Loader2 } from "lucide-react";
import { RiskBadge } from "../components/RiskBadge";
import { Card, CardContent } from "../components/Card";
import { Button } from "../components/Button";
import { useState } from "react";
import { WebsiteAiInsight } from "../components/WebsiteAiInsight";

interface ScanResult {
  total_items: number;
  analyzed_items: any[];
  summary: {
    total_items: number;
    high_risk_count: number;
    avg_risk_score: number;
    scanner: {
      website_report: {
        url: string;
        security_headers: {
          present: Record<string, any>;
          missing: Record<string, any>;
          issues: string[];
        };
        cookie_issues: any[];
        tracking_scripts: any[];
        vulnerable_libraries: any[];
        risk_score: number;
        overall_risk_level: string;
      };
    };
  };
  recommendations: string[];
}

export function WebsiteScanResults() {
  const [expandedInsight, setExpandedInsight] = useState<string | null>(null);
  const [url, setUrl] = useState("");
  const [isScanning, setIsScanning] = useState(false);
  const [scanResult, setScanResult] = useState<ScanResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  const toggleInsight = (id: string) => {
    setExpandedInsight(expandedInsight === id ? null : id);
  };

  const handleScan = async () => {
    setIsScanning(true);
    setError(null);

    try {
      const response = await fetch("http://localhost:8000/scan/website", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url }),
      });

      if (!response.ok) {
        throw new Error("Scan failed");
      }

      const data = await response.json();
      setScanResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to scan website");
    } finally {
      setIsScanning(false);
    }
  };

  return (
    <div className="w-full min-h-screen">
      <div className="w-full px-8 space-y-8 animate-in fade-in duration-500 py-8">
        {/* Header */}
        <div className="space-y-6">
          <div>
            <h2 className="text-2xl font-bold text-gray-900">Website Privacy Scan</h2>
            <p className="text-gray-500">Analysis of external trackers and data collection practices</p>
          </div>

          <div className="bg-[#f5f8ff] border border-[#e2e8f0] rounded-2xl p-8 shadow-sm w-full">
            <div className="flex flex-col gap-4">
              <div className="flex items-center gap-3">
                <Globe className="size-6 text-gray-800" strokeWidth={2.5} />
                <h3 className="text-lg font-bold text-gray-900">Analyze Website</h3>
              </div>
              <div className="flex gap-3 mt-2 w-full min-w-0">
                <div className="flex-1 min-w-0 bg-white border border-gray-200 rounded-xl px-4 py-3 flex items-center gap-2 shadow-sm">
                  <Search className="size-4 text-gray-400" />
                  <input
                    type="text"
                    className="bg-transparent border-none outline-none w-full text-gray-700 text-sm min-w-0"
                    value={url}
                    onChange={(e) => setUrl(e.target.value)}
                    placeholder="Enter website URL (e.g., https://example.com)"
                    disabled={isScanning}
                  />
                </div>
                <Button
                  size="lg"
                  icon={isScanning ? Loader2 : Play}
                  className={`bg-[#1a68ff] hover:bg-[#0052cc] rounded-lg px-8 font-semibold shadow-md disabled:opacity-50 ${isScanning ? '[&>svg]:animate-spin' : ''}`}
                  onClick={handleScan}
                  disabled={isScanning}
                >
                  {isScanning ? "Scanning..." : "Run Scan"}
                </Button>
              </div>
              {error && (
                <div className="mt-3 p-3 bg-red-50 border border-red-200 rounded-lg flex items-center gap-2">
                  <AlertTriangle className="size-4 text-red-600" />
                  <p className="text-sm text-red-600 font-medium">{error}</p>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Summary Metrics Grid */}
        {!scanResult && !isScanning && (
          <div className="w-full text-center py-16">
            <Globe className="size-16 text-gray-300 mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-gray-600 mb-2">No scan results yet</h3>
            <p className="text-gray-400">Enter a website URL and click "Run Scan" to begin analysis</p>
          </div>
        )}

        {scanResult && (
          <>
            <div className="w-full grid grid-cols-1 md:grid-cols-3 gap-6">
              {[
                {
                  label: "Security Issues",
                  value: scanResult.total_items.toString(),
                  desc: "Total findings detected",
                  icon: <ShieldAlert className="size-5 text-red-600" />,
                },
                {
                  label: "High Risk Items",
                  value: scanResult.summary.high_risk_count.toString(),
                  desc: "Critical security concerns",
                  icon: <AlertTriangle className="size-5 text-red-600" />,
                },
                {
                  label: "Risk Score",
                  value: Math.round(scanResult.summary.scanner.website_report.risk_score).toString(),
                  desc: `Overall risk level: ${scanResult.summary.scanner.website_report.overall_risk_level}`,
                  icon: <Globe className="size-5 text-red-600" />,
                },
              ].map((stat) => (
                <Card key={stat.label} className="shadow-sm">
                  <CardContent className="pt-6">
                    <div className="flex items-center gap-2 mb-6">
                      {stat.icon}
                      <span className="text-gray-900 font-bold text-sm">{stat.label}</span>
                    </div>

                    <p className="text-3xl font-bold text-red-600">
                      {stat.value}
                    </p>
                    <p className="text-[11px] text-gray-400 font-bold mt-1 uppercase">
                      {stat.desc}
                    </p>
                  </CardContent>
                </Card>
              ))}
            </div>

            <section className="w-full space-y-4">
              <div className="flex items-center gap-2">
                <ShieldAlert className="size-6 text-red-600" />
                <h3 className="text-xl font-bold text-gray-900">Vulnerability Details</h3>
              </div>

              {/* Render analyzed items dynamically */}
              {scanResult.analyzed_items.map((item, index) => {
                const riskVariant = item.risk_assessment.risk_level === 'critical' ? 'critical' :
                  item.risk_assessment.risk_level === 'high' ? 'high' : 'medium';
                const riskLabel = item.risk_assessment.risk_level.charAt(0).toUpperCase() +
                  item.risk_assessment.risk_level.slice(1);

                return (
                  <Card key={index} className="border-[#ffe4d6] bg-white rounded-2xl overflow-hidden shadow-sm w-full">
                    <CardContent className="p-6">
                      <div className="flex items-center gap-3 mb-4">
                        <span className="text-lg font-bold text-gray-900">{item.name}</span>
                        <RiskBadge variant={riskVariant} className="bg-[#fff1e7] text-[#d97706] border-none font-bold">
                          {riskLabel}
                        </RiskBadge>
                      </div>
                      <div className="space-y-2 text-sm text-gray-600 mb-6">
                        <p>
                          <span className="font-medium text-gray-400">Finding:</span>
                          <span className="ml-2 font-medium text-gray-700">{item.value}</span>
                        </p>
                        <p>
                          <span className="font-medium text-gray-400">Risk Score:</span>
                          <span className="ml-2 font-bold text-red-500">{item.risk_assessment.risk_score}/10</span>
                        </p>
                      </div>

                      {/* AI Privacy Insight */}
                      <div className="mt-4 pt-4 border-t border-gray-100 w-full">
                        <button
                          onClick={() => toggleInsight(`item-${index}`)}
                          className="flex items-center justify-between w-full px-4 py-3 bg-[#fafafa] rounded-xl border border-gray-100 group">
                          <div className="flex items-center gap-2 text-[#8b5cf6] font-semibold text-sm">
                            <Sparkles className="size-4 fill-current" /> AI Privacy Insight
                          </div>
                          <ChevronDown className={`size-4 text-gray-400 transition-transform ${expandedInsight === `item-${index}` ? 'rotate-180' : ''
                            }`} />
                        </button>
                        <div
                          className={`w-full overflow-hidden transition-[max-height] duration-300 ease-in-out ${expandedInsight === `item-${index}` ? 'max-h-[1000px]' : 'max-h-0'
                            }`}
                        >
                          <WebsiteAiInsight
                            analysis={item.classification.reasoning}
                            risks={item.risk_assessment.risk_factors}
                            recommendations={item.suggestions.map((s: any) => s.action)}
                          />
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                );
              })}

              {/* Overall Recommendations */}
              {scanResult.recommendations.length > 0 && (
                <Card className="border-blue-200 bg-blue-50 rounded-2xl overflow-hidden shadow-sm w-full">
                  <CardContent className="p-6">
                    <div className="flex items-center gap-3 mb-4">
                      <CheckCircle2 className="size-5 text-blue-600" />
                      <span className="text-lg font-bold text-gray-900">Overall Recommendations</span>
                    </div>
                    <ul className="space-y-2">
                      {scanResult.recommendations.map((rec, i) => (
                        <li key={i} className="flex items-start gap-3 text-sm text-gray-700">
                          <span className="mt-1.5 size-1.5 rounded-full bg-blue-600 shrink-0" />
                          {rec}
                        </li>
                      ))}
                    </ul>
                  </CardContent>
                </Card>
              )}
            </section>
          </>
        )}
      </div>
    </div>
  );
}