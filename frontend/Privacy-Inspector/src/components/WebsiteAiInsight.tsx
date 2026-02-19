import { Sparkles } from "lucide-react";

interface WebsiteAiInsightProps {
  type: 'headers' | 'cookies'; 
}

export function WebsiteAiInsight({ type }: WebsiteAiInsightProps) {
  const getInsight = () => {
    if (type === 'headers') {
      return {
        analysis: "Your site is missing critical security headers like CSP and HSTS. This makes your visitors vulnerable to Man-in-the-Middle (MitM) interceptions and Cross-Site Scripting (XSS) where attackers can inject malicious scripts.",
        recommendations: [
          "Configure 'Content-Security-Policy' to restrict script sources",
          "Enable 'Strict-Transport-Security' (HSTS) for forced HTTPS",
          "Add 'X-Content-Type-Options: nosniff' to prevent MIME sniffing"
        ]
      };
    } else {
      return {
        analysis: "Detected cookies (AWSALB) are missing 'HttpOnly' and 'Secure' flags. Without these, scripts can read your session tokens, and data could be sent over unencrypted connections, leading to potential session hijacking.",
        recommendations: [
          "Set 'HttpOnly' flag to prevent JavaScript cookie access",
          "Enable 'Secure' flag to ensure cookies are only sent over HTTPS",
          "Implement 'SameSite=Lax' to mitigate Cross-Site Request Forgery"
        ]
      };
    }
  };

  const insight = getInsight();

  return (
    <div className="mt-3 p-4 bg-[#f8f5ff] border border-[#e9d5ff] rounded-xl space-y-4 animate-in zoom-in-95 duration-300">
      {/* Analysis Section */}
      <div>
        <div className="flex items-center gap-2 mb-2">
          <Sparkles className="size-4 text-[#8b5cf6] fill-current" />
          <h5 className="font-bold text-[#5b21b6] text-xs uppercase tracking-wider">AI Analysis</h5>
        </div>
        <p className="text-sm text-[#6d28d9] leading-relaxed font-medium">
          {insight.analysis}
        </p>
      </div>

      {/* Divider */}
      <div className="h-px bg-[#ddd6fe]" />

      {/* Recommendations Section */}
      <div>
        <h5 className="font-bold text-[#5b21b6] text-sm mb-3 underline decoration-[#ddd6fe] underline-offset-4">
          Recommendations
        </h5>
        <ul className="space-y-2.5">
          {insight.recommendations.map((rec, i) => (
            <li key={i} className="flex items-start gap-3 text-sm text-[#7c3aed] font-medium">
              <span className="mt-1.5 size-1.5 rounded-full bg-[#8b5cf6] shrink-0 shadow-[0_0_8px_rgba(139,92,246,0.4)]" />
              {rec}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}