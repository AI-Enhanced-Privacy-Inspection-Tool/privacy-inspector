import { ShieldCheck, AlertCircle, Cookie, Fingerprint, Database, CheckCircle2, FolderOpen } from "lucide-react";
import { RiskBadge } from "../components/RiskBadge";
import { Card, CardHeader, CardContent, CardTitle, CardDescription, CardAction } from "../components/Card";

export function ScanResults() {
  return (
    <div className="space-y-8 animate-in fade-in duration-500">  
      {/* Header */}
      <div>
        <h2 className="text-2xl font-bold text-gray-900">
          Privacy Scan Results
        </h2>
        <p className="text-gray-500">
          Summary of privacy issues detected in your system
        </p>
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
              Jan 29, 2026, 1:30 PM
            </p>

            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-6">
              {[
                { label: "Cookies", value: "8" },
                { label: "Identifiers", value: "6" },
                { label: "Apps Scanned", value: "6" },
                { label: "Total Data", value: "8.5 MB" },
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
      <Card className="bg-red-50 border-red-100 shadow-sm">
        <CardContent className="pt-6 flex items-center gap-4">
          <div className="bg-white rounded-full p-1 border border-red-200">
            <AlertCircle className="w-6 h-6 text-red-600" />
          </div>

          <div>
            <p className="text-red-900 font-bold">
              11 Privacy Issues Detected
            </p>
            <p className="text-red-700 text-sm font-medium">
              High and critical risk items requiring attention
            </p>
          </div>
        </CardContent>
      </Card>

      {/* Summary Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {[
          {
            label: "Tracking Cookies",
            value: "1",
            desc: "High-risk cookies found",
            icon: <Cookie className="w-5 h-5 text-red-600" />,
          },
          {
            label: "Identifiers",
            value: "1",
            desc: "Persistent tracking identifiers",
            icon: <Fingerprint className="w-5 h-5 text-red-600" />,
          },
          {
            label: "App Data",
            value: "1",
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
      <section className="space-y-4">
        <div className="flex items-center gap-2">
          <Cookie className="w-6 h-6 text-red-600" />
          <h3 className="text-xl font-bold text-gray-900">
            High-Risk Cookies
          </h3>
        </div>

        <Card className="shadow-sm">
          <CardHeader>
            <div className="flex items-center gap-3">
              <CardTitle className="text-gray-800 font-mono text-lg font-medium">
                fr
              </CardTitle>

              <CardAction className="flex gap-2">
                <RiskBadge variant="high">High Risk</RiskBadge>
                <RiskBadge variant="info">advertising</RiskBadge>
              </CardAction>
            </div>

            <CardDescription className="text-gray-500 font-medium">
              .facebook.com
            </CardDescription>
          </CardHeader>

          <CardContent className="space-y-4">
            <div className="bg-slate-50 p-4 rounded-lg border border-slate-100">
              <p className="text-sm text-slate-700">
                <span className="font-bold">Problem:</span> Facebook advertising
                cookie used for cross-site tracking and ad targeting.
              </p>

              <div className="flex gap-6 mt-3 text-xs text-slate-400 font-medium">
                <span>Size: 256 B</span>
                <span>Expires: 4/29/2026</span>
                <span className="flex items-center gap-1 text-green-600">
                  <CheckCircle2 className="w-3 h-3" /> Secure: ✓
                </span>
                <span className="flex items-center gap-1 text-green-600">
                  <CheckCircle2 className="w-3 h-3" /> HttpOnly: ✓
                </span>
              </div>
            </div>
          </CardContent>
        </Card>
      </section>

      {/* Persistent Identifiers */}
      <section className="space-y-4">
        <div className="flex items-center gap-2">
          <Fingerprint className="w-6 h-6 text-red-600" />
          <h3 className="text-xl font-bold text-gray-900">
            Persistent Identifiers
          </h3>
        </div>

        <Card className="shadow-sm">
          <CardHeader>
            <div className="flex items-center gap-3">
              <CardTitle className="text-gray-800 font-mono text-lg font-medium">
                FINGERPRINT
              </CardTitle>

              <CardAction className="flex gap-2">
                <RiskBadge variant="critical">Critical Risk</RiskBadge>
                <RiskBadge variant="persistent">Persistent</RiskBadge>
              </CardAction>
            </div>

            <CardDescription className="text-gray-500 font-medium">
              Canvas Fingerprinting (multiple sites)
            </CardDescription>
          </CardHeader>

          <CardContent>
            <div className="bg-slate-50 p-4 rounded-lg border border-slate-100">
              <p className="text-sm text-slate-700">
                <span className="font-bold">Problem:</span> Browser fingerprint
                detected. This unique identifier can track you across websites
                even without cookies.
              </p>

              <div className="mt-3 text-xs text-slate-400 font-medium">
                Value: fp_a1b2c3d4e5f6... | Last Seen: Jan 29, 2026, 12:30 PM
              </div>
            </div>
          </CardContent>
        </Card>
      </section>

      {/* Applications */}
      <section className="space-y-4">
        <div className="flex items-center gap-2">
          <Database className="w-6 h-6 text-red-600" />
          <h3 className="text-xl font-bold text-gray-900">
            Applications with Privacy Concerns
          </h3>
        </div>

        <Card className="shadow-sm">
          <CardHeader>
            <div className="flex items-center gap-3">
              <CardTitle className="text-gray-800 font-mono text-lg font-medium">
                Google Chrome
              </CardTitle>

              <CardAction className="flex gap-2">
                <RiskBadge variant="high">High Risk</RiskBadge>
                <RiskBadge variant="pii">Contains PII</RiskBadge>
              </CardAction>
            </div>

            <CardDescription className="text-gray-500 font-medium">
              /Users/user/Library/Application Support/Google/Chrome
            </CardDescription>
          </CardHeader>

          <CardContent className="space-y-4">
            <div className="bg-slate-50 p-4 rounded-lg border border-slate-100 space-y-3">
              <p className="text-sm text-slate-700">
                <span className="font-bold">Problem:</span> Chrome stores
                extensive user data including browsing history and auto-fill
                information.
              </p>

              <div className="flex flex-wrap gap-2">
                {["Cookies", "Cache", "History", "LocalStorage", "IndexedDB"].map(
                  (tag) => (
                    <RiskBadge
                      key={tag}
                      variant="info"
                      className="bg-slate-200 text-slate-700 normal-case font-medium"
                    >
                      {tag}
                    </RiskBadge>
                  )
                )}
              </div>

              <p className="text-xs text-slate-400 font-medium">
                Total Size: 2.3 MB
              </p>
            </div>
          </CardContent>
        </Card>
      </section>
    </div>
  );
}
