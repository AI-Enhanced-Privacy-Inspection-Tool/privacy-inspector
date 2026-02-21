import { Loader2, XCircle } from "lucide-react";
import { Card, CardContent } from "./Card";
import { Button } from "./Button";

interface LoadingScanProps {
  onStop?: () => void;
}

const LoadingScan = ({ onStop }: LoadingScanProps) => {
  return (
    <div className="space-y-8 animate-in fade-in duration-60">
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


        {/* Loading Card */}
        <Card className="bg-[#f5f8ff] border border-[#e2e8f0] rounded-2xl shadow-none">
          <CardContent className="py-20 flex flex-col items-center justify-center text-center">
            
            {/* Animated Spinner */}
            <div className="mb-6">
              <Loader2 
                className="size-12 text-[#1a68ff] animate-spin" 
                strokeWidth={2.5} 
              />
            </div>

            {/* Scanning Title */}
            <h3 className="text-2xl font-bold text-gray-900 mb-4">
              Scanning Your System...
            </h3>

            {/* Description Text */}
            <p className="text-gray-500 max-w-lg text-lg leading-relaxed mb-8">
              Analyzing browser cookies, local storage, session data, and 
              application privacy settings. This may take a few moments.
            </p>

            {/* Progress Checklist */}
            <div className="flex flex-col gap-3 text-left mb-10">
              {[
                "Scanning browser data...",
                "Analyzing cookies and trackers...",
                "Checking application permissions..."
              ].map((text, i) => (
                <div key={i} className="flex items-center gap-3 text-gray-500">
                  <div className="size-2 bg-[#1a68ff] rounded-full animate-pulse" />
                  <span className="text-md">{text}</span>
                </div>
              ))}
            </div>

            {/* Stop Scan Button */}
            {onStop && (
              <Button 
                variant="outline"
                size="lg"
                onClick={onStop}
                icon={XCircle}
                className="border-red-200 text-red-600 hover:bg-red-50 hover:text-red-700 bg-white px-8"
              >
                Stop Scan
              </Button>
            )}

          </CardContent>
        </Card>
      </div>
    </div>
  );
};


export default LoadingScan; 