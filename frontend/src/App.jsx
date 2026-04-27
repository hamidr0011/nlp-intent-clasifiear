import { useState } from 'react';
import { Circle, Square, Triangle, ArrowRight, Activity } from 'lucide-react';

function App() {
  const [inputText, setInputText] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handlePredict = async (e) => {
    e.preventDefault();
    if (!inputText.trim()) return;

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await fetch('http://127.0.0.1:5000/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: inputText }),
      });
      
      const data = await response.json();
      
      if (!response.ok) {
        throw new Error(data.error || 'Prediction failed');
      }
      
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col">
      {/* Navigation */}
      <nav className="w-full bg-white border-b-4 border-bauhaus-black px-6 py-4 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className="flex items-center">
            <Circle className="w-8 h-8 fill-bauhaus-red text-bauhaus-black" strokeWidth={3} />
            <Square className="w-8 h-8 fill-bauhaus-blue text-bauhaus-black -ml-2" strokeWidth={3} />
            <Triangle className="w-8 h-8 fill-bauhaus-yellow text-bauhaus-black -ml-2" strokeWidth={3} />
          </div>
          <span className="font-black text-2xl uppercase tracking-tighter ml-2">NLU Engine</span>
        </div>
      </nav>

      {/* Hero Section */}
      <main className="flex-grow flex flex-col md:flex-row divide-y-4 md:divide-y-0 md:divide-x-4 divide-bauhaus-black">
        
        {/* Left Form Area */}
        <div className="flex-1 p-8 md:p-16 bg-canvas flex flex-col justify-center relative overflow-hidden">
          <div className="absolute inset-0 bg-dot-pattern opacity-10"></div>
          
          <div className="relative z-10 max-w-2xl">
            <h1 className="text-6xl md:text-8xl font-black uppercase tracking-tighter leading-[0.9] mb-8">
              Analyze <br/>
              <span className="text-bauhaus-red">Intent</span> <br/>
              Instantly
            </h1>
            
            <p className="text-lg md:text-xl font-bold mb-12 uppercase tracking-widest text-gray-700">
              60 Classes. Millisecond Latency.
            </p>

            <form onSubmit={handlePredict} className="flex flex-col gap-6">
              <div className="relative">
                <input 
                  type="text" 
                  value={inputText}
                  onChange={(e) => setInputText(e.target.value)}
                  placeholder="e.g., Switch off the bedroom lights"
                  className="w-full p-6 text-xl md:text-2xl font-medium border-4 border-bauhaus-black bg-white focus:outline-none focus:ring-0 focus:shadow-bauhaus-lg transition-shadow"
                />
                {/* Decorative shape */}
                <div className="absolute -top-4 -right-4 w-8 h-8 bg-bauhaus-yellow border-4 border-bauhaus-black rounded-full shadow-bauhaus-sm"></div>
              </div>
              
              <button 
                type="submit" 
                disabled={loading}
                className="self-start px-8 py-4 bg-bauhaus-blue text-white font-bold text-xl uppercase tracking-widest border-4 border-bauhaus-black shadow-bauhaus-lg flex items-center gap-3 transition-all duration-200 ease-out active:translate-x-[4px] active:translate-y-[4px] active:shadow-none hover:-translate-y-1 disabled:opacity-70 disabled:cursor-not-allowed"
              >
                {loading ? 'Processing...' : 'Predict Intent'}
                {!loading && <ArrowRight strokeWidth={3} />}
              </button>
            </form>

            {error && (
              <div className="mt-8 p-4 bg-bauhaus-red text-white font-bold border-4 border-bauhaus-black uppercase">
                ERROR: {error}
              </div>
            )}
          </div>
        </div>

        {/* Right Results Area */}
        <div className="w-full md:w-[45%] bg-bauhaus-yellow p-8 md:p-16 flex flex-col items-center justify-center relative">
          {/* Bauhaus Abstract background shapes */}
          <div className="absolute top-10 right-10 w-64 h-64 border-8 border-bauhaus-black rounded-full opacity-20 pointer-events-none"></div>
          <div className="absolute bottom-10 left-10 w-48 h-48 border-8 border-bauhaus-black rotate-45 opacity-20 pointer-events-none"></div>

          {!result && !loading && (
             <div className="relative z-10 text-center">
               <Activity className="w-24 h-24 mx-auto mb-6 opacity-30" strokeWidth={2}/>
               <h2 className="text-3xl font-black uppercase tracking-tighter opacity-50">Awaiting Input</h2>
             </div>
          )}

          {loading && (
             <div className="relative z-10 text-center animate-pulse">
               <div className="w-24 h-24 border-8 border-bauhaus-black border-t-bauhaus-red rounded-full animate-spin mx-auto mb-6"></div>
               <h2 className="text-3xl font-black uppercase tracking-tighter">Analyzing...</h2>
             </div>
          )}

          {result && (
            <div className="relative z-10 w-full max-w-md bg-white border-4 border-bauhaus-black shadow-bauhaus-lg p-8 hover:-translate-y-2 transition-transform duration-300 ease-out">
              <div className="absolute -top-6 -left-6 w-12 h-12 bg-bauhaus-red border-4 border-bauhaus-black"></div>
              
              <h3 className="text-sm font-black uppercase tracking-widest mb-2 text-gray-500">Predicted Intent</h3>
              <div className="text-4xl md:text-5xl font-black uppercase tracking-tighter leading-tight mb-8 break-words text-bauhaus-blue">
                {result.intent}
              </div>

              <div className="border-t-4 border-bauhaus-black pt-6">
                <h3 className="text-sm font-black uppercase tracking-widest mb-2 text-gray-500">Confidence Score</h3>
                <div className="flex items-end gap-2">
                  <span className="text-5xl font-black">{Math.round(result.confidence * 100)}</span>
                  <span className="text-2xl font-bold mb-1">%</span>
                </div>
                
                {/* Visual Confidence Bar */}
                <div className="w-full h-4 border-2 border-bauhaus-black mt-4 bg-gray-200">
                  <div 
                    className="h-full bg-bauhaus-red border-r-2 border-bauhaus-black" 
                    style={{ width: `${result.confidence * 100}%` }}
                  ></div>
                </div>
              </div>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}

export default App;
