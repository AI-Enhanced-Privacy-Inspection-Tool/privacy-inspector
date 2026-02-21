import { Globe, ShieldAlert, Search,  Play, Sparkles, ChevronDown, Lock } from "lucide-react";
import { RiskBadge } from "../components/RiskBadge";
import { Card, CardContent } from "../components/Card";
import { Button } from "../components/Button";
import { useState } from "react";
import { WebsiteAiInsight } from "../components/WebsiteAiInsight"; 

export function WebsiteScanResults() {
  const [expandedInsight, setExpandedInsight] = useState<string | null>(null);

  const toggleInsight = (id: string) => {
    setExpandedInsight(expandedInsight === id ? null : id);
  };

  return (
    <div className="w-full max-w-7xl mx-auto px-6 space-y-8 animate-in fade-in duration-500">  
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
                  defaultValue="https://ginandjuice.shop"
                />
              </div>
              <Button size="lg" icon={Play} className="bg-[#1a68ff] hover:bg-[#0052cc] rounded-lg px-8 font-semibold shadow-md">
                Run Scan
              </Button>
            </div>
          </div>
        </div>
      </div>

      {/* Summary Metrics Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {[
          {
            label: "Header Issues",
            value: "4",
            desc: "Missing critical security headers",
            icon: <ShieldAlert className="size-5 text-red-600" />,
          },
          {
            label: "Cookie Risks",
            value: "2",
            desc: "Insecure flags detected",
            icon: <Lock className="size-5 text-red-600" />,
          },
          {
            label: "Risk Score",
            value: "36",
            desc: "Overall vulnerability rating",
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

      <section className="space-y-4">
        <div className="flex items-center gap-2">
          <ShieldAlert className="size-6 text-red-600" />
          <h3 className="text-xl font-bold text-gray-900">Vulnerability Details</h3>
        </div>

        {/* Security Headers */}
        <Card className="border-[#ffe4d6] bg-white rounded-2xl overflow-hidden shadow-sm w-full">
          <CardContent className="p-6">
            <div className="flex items-center gap-3 mb-4">
              <span className="text-lg font-bold text-gray-900">Security Header Deficiencies</span>
              <RiskBadge variant="high" className="bg-[#fff1e7] text-[#d97706] border-none font-bold">Critical</RiskBadge>
            </div>
            <div className="space-y-2 text-sm text-gray-600 mb-6">
              <p><span className="font-medium text-gray-400">Finding:</span> <span className="ml-2 font-medium text-gray-700">Missing CSP, HSTS, and X-Content-Type headers</span></p>
              <p><span className="font-medium text-gray-400">Status:</span> <span className="ml-2 font-bold text-red-500 underline decoration-2 underline-offset-4">Vulnerable to XSS & Interception</span></p>
            </div>

            {/* AI Privacy Insight */}
            <div className="mt-4 pt-4 border-t border-gray-100 w-full">
                <button 
                  onClick={() => toggleInsight('headers')} 
                  className="flex items-center justify-between w-full px-4 py-3 bg-[#fafafa] rounded-xl border border-gray-100 group">
                    <div className="flex items-center gap-2 text-[#8b5cf6] font-semibold text-sm">
                      <Sparkles className="size-4 fill-current" /> AI Privacy Insight
                    </div>
                    <ChevronDown className={`size-4 text-gray-400 transition-transform ${expandedInsight === 'cookie-1' ? 'rotate-180' : ''}`} />
                  </button>
                  <div
                    className={`w-full overflow-hidden transition-[max-height] duration-300 ease-in-out ${
                      expandedInsight === 'headers' ? 'max-h-[1000px]' : 'max-h-0'
                    }`}
                  >
                    <WebsiteAiInsight type="headers" />
                  </div>
            </div>
          </CardContent>
        </Card>

        {/* Cookie Issues */}
        <Card className="border-[#ffe4d6] bg-white rounded-2xl overflow-hidden shadow-sm w-full">
          <CardContent className="p-6">
            <div className="flex items-center gap-3 mb-4">
              <span className="text-lg font-bold text-gray-900">Insecure Cookie: AWSALB</span>
              <RiskBadge variant="high" className="bg-[#fff1e7] text-[#d97706] border-none font-bold">High Risk</RiskBadge>
            </div>
            <div className="space-y-2 text-sm text-gray-600 mb-6">
              <p><span className="font-medium text-gray-400">Finding:</span> <span className="ml-2 font-medium text-gray-700">Missing HttpOnly & Secure flags</span></p>
              <p><span className="font-medium text-gray-400">Status:</span> <span className="ml-2 font-bold text-red-500 underline decoration-2 underline-offset-4">Vulnerable to Session Hijacking</span></p>
            </div>

            {/* AI Privacy Insight */}
            <div className="mt-4 pt-4 border-t border-gray-100 w-full">
                <button 
                  onClick={() => toggleInsight('cookies')} 
                  className="flex items-center justify-between w-full px-4 py-3 bg-[#fafafa] rounded-xl border border-gray-100 group">
                    <div className="flex items-center gap-2 text-[#8b5cf6] font-semibold text-sm">
                      <Sparkles className="size-4 fill-current" /> AI Privacy Insight
                    </div>
                    <ChevronDown className={`size-4 text-gray-400 transition-transform ${expandedInsight === 'cookie-1' ? 'rotate-180' : ''}`} />
                  </button>
                  <div
                    className={`w-full overflow-hidden transition-[max-height] duration-300 ease-in-out ${
                      expandedInsight === 'cookies' ? 'max-h-[1000px]' : 'max-h-0'
                    }`}
                  >
                    <WebsiteAiInsight type="cookies" />
                  </div>
            </div>
          </CardContent>
        </Card>
      </section>
    </div>
  );
}