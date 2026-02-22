import { Sparkles, AlertTriangle } from "lucide-react";

interface LocalAiInsightProps {
  item: any;
}

export function LocalAiInsight({ item }: LocalAiInsightProps) {
  const classification = item.classification || {};
  const riskAssessment = item.risk_assessment || {};
  const suggestions = item.suggestions || [];

  return (
    <div className="mt-3 p-5 bg-[#f8f5ff] border border-[#e9d5ff] rounded-xl space-y-4 animate-in zoom-in-95 duration-300">
      {/* Classification Section */}
      <div>
        <div className="flex items-center gap-2 mb-2">
          <Sparkles className="size-4 text-[#8b5cf6] fill-current" />
          <h5 className="font-bold text-[#5b21b6] text-sm uppercase tracking-wider">AI Analysis</h5>
        </div>
        <p className="text-sm text-[#6d28d9] leading-relaxed mb-3">
          {classification.reasoning || 'No AI analysis available.'}
        </p>

        {/* Classification Badges */}
        <div className="flex flex-wrap gap-2 mt-2">
          {classification.contains_pii && (
            <span className="px-2 py-1 bg-red-100 text-red-700 text-xs font-semibold rounded-full">
              Contains PII: {classification.pii_types?.join(', ')}
            </span>
          )}
          {classification.is_tracking_data && (
            <span className="px-2 py-1 bg-orange-100 text-orange-700 text-xs font-semibold rounded-full">
              Tracking Data
            </span>
          )}
          <span className="px-2 py-1 bg-purple-100 text-purple-700 text-xs font-semibold rounded-full capitalize">
            {classification.sensitivity_level} Sensitivity
          </span>
        </div>
      </div>

      {/* Divider */}
      <div className="h-px bg-[#ddd6fe]" />

      {/* Risk Assessment */}
      {riskAssessment.risk_factors && riskAssessment.risk_factors.length > 0 && (
        <div>
          <div className="flex items-center gap-2 mb-2">
            <AlertTriangle className="size-4 text-orange-600" />
            <h5 className="font-bold text-[#5b21b6] text-sm">Risk Factors</h5>
          </div>
          <ul className="space-y-2">
            {riskAssessment.risk_factors.map((factor: string, idx: number) => (
              <li key={idx} className="flex items-start gap-2 text-sm text-[#7c3aed]">
                <span className="mt-1 size-1.5 rounded-full bg-orange-500 shrink-0" />
                {factor}
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Divider */}
      {suggestions.length > 0 && <div className="h-px bg-[#ddd6fe]" />}

      {/* Suggestions Section */}
      {suggestions.length > 0 && (
        <div>
          <h5 className="font-bold text-[#5b21b6] text-sm mb-2">AI Suggestions</h5>
          {suggestions.map((suggestion: any, idx: number) => (
            <div key={idx} className="mb-3 last:mb-0">
              <div className="flex items-center gap-2 mb-1">
                <span className={`px-2 py-0.5 text-xs font-bold rounded capitalize ${suggestion.priority === 'high' ? 'bg-red-100 text-red-700' :
                    suggestion.priority === 'medium' ? 'bg-orange-100 text-orange-700' :
                      'bg-green-100 text-green-700'
                  }`}>
                  {suggestion.action}
                </span>
                <span className="text-xs text-purple-600 capitalize">({suggestion.priority} priority)</span>
              </div>
              <p className="text-sm text-[#6d28d9] leading-relaxed">
                {suggestion.reasoning}
              </p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}