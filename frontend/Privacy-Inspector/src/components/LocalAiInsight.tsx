import { Sparkles } from "lucide-react";

interface LocalAiInsightProps {
  type: 'cookie' | 'identifier' | 'app';
}

export function LocalAiInsight({ type }: LocalAiInsightProps) {
  const getAiInsight = () => {
    if (type === 'cookie') {
      return {
        analysis: "This advertising cookie was detected via key_name matching. It indicates active cross-site tracking which builds a profile of your browsing habits over time.",
        recommendations: [
          "Clear browser cookies and cache immediately",
          "Block third-party cookies in browser settings",
          "Use a privacy-focused extension to auto-delete trackers"
        ]
      };
    } else if (type === 'identifier') {
      return {
        analysis: "A high-confidence persistent identifier was found in your local storage. Unlike standard cookies, these often persist even after clearing browser history.",
        recommendations: [
          "Manually audit local storage via developer tools",
          "Enable 'Canvas' protection in your browser",
          "Use a VPN to prevent network-level fingerprinting"
        ]
      };
    } else {
      return {
        analysis: "This application path contains PII (Personally Identifiable Information). The presence of 'accounts.app.username' suggests local caching of sensitive credentials.",
        recommendations: [
          "Review the application's local data storage policy",
          "Disable 'Remember Me' features in the app",
          "Encrypt your local disk to protect idle application data"
        ]
      };
    }
  };

  const insight = getAiInsight();

  return (
    <div className="mt-3 p-4 bg-[#f8f5ff] border border-[#e9d5ff] rounded-xl space-y-4 animate-in zoom-in-95 duration-300">
      {/* Analysis Section */}
      <div>
        <div className="flex items-center gap-2 mb-2">
          <Sparkles className="size-4 text-[#8b5cf6] fill-current" />
          <h5 className="font-bold text-[#5b21b6] text-sm uppercase tracking-wider">AI Analysis</h5>
        </div>
        <p className="text-sm text-[#6d28d9] leading-relaxed">
          {insight.analysis}
        </p>
      </div>

      {/* Divider */}
      <div className="h-px bg-[#ddd6fe]" />

      {/* Recommendations Section */}
      <div>
        <h5 className="font-bold text-[#5b21b6] text-sm mb-2">Recommendations</h5>
        <ul className="space-y-2">
          {insight.recommendations.map((rec, idx) => (
            <li key={idx} className="flex items-start gap-2 text-sm text-[#7c3aed]">
              <span className="mt-1 size-1.5 rounded-full bg-[#8b5cf6] shrink-0" />
              {rec}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}