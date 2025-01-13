import React, {useState, useEffect} from "react"
const App = () => {
  const [games, setGames] = useState([]);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);


  const fetchGames = async () => {
    if (!search.trim()){
      setError("Please enter a search term");
      return;
    }

    try{
      setLoading(true)
      setError(null);
      const response = await fetch(`http://127.0.0.1:5000/games?search=${encodeURIComponent(search)}`);
      if (!response.ok){
        const errorData = await response.json().catch(() => null);
        throw new Error(errorData?.error || `HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      if (Array.isArray(data)){
        setGames(data);
        if (data.length === 0){
          setError("No games found for your search term");
        }
      } else {
        throw new Error("Invalid response format from server");
      }
      

    } catch (error){
      setError(error.message || "Failed to fetch games. Please try again.");
      console.error("Error fetching games:", error);
    } finally {
      setLoading(false);
    }
  };
  const handleSubmit = (e) => {
    e.preventDefault();
    fetchGames();
  };

  const formatDate = (timestamp) => {
    if (!timestamp) return "Unknown";
    return new Date(timestamp * 1000).toLocaleDateString();
  };


  return (
    <div className="p-4 max-w-4x1 mx-auto">
    <div className="bg-white rounded-lg shadow-md p-6 mb-6">
      <h1 className="text-3xl font-bold mb-4">Video Game Search Engine</h1>
      <form onSubmit={handleSubmit} className="flex gap-2">
        <input
        type="text"
        placeholder="Search for a game"
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        className="flex-1 px-4 py-2 border rounded-md"
        />
        <button 
        type="submit"
        disabled={loading}
        className="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 disabled:bg-blue-300"
        >
          {loading ? "Searching..." : "Search"}
        </button>
        </form>
      </div>
    {error && (
      <div className="text-red-500 mb-4 p-4 bg-red-50 rounded-md">
        {error}
        </div>
    )}

    <div className="space-y-4">
      {games.map((game,index) => (
        <div key={index} className="bg-white rounded-lg shadow-mid p-6">
          <h3 className="text-xl font-semibold mb-2">{game.name}</h3>
          <p className="text-gray-600 mb-2">
            Release Date: {formatDate(game.first_release_date)}
          </p>
          <p className="text-gray-700">
            {game.summary || "No description available"}
          </p>
          </div>
      ))}
    </div>
    </div>
    

    
  );
};
export default App;
