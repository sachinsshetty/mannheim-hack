import { Component, ChangeEvent } from 'react';
import axios from 'axios';
import { AxiosError } from 'axios';
import './App.css'

interface AppState {
  response: any;
  isLoading: boolean;
  models: string[]; 
  selectedModel: string; 
}

class App extends Component<{}, AppState> {
  ollamaBaseUrl = import.meta.env.VITE_OLLAMA_BASE_URL;
  constructor(props:{}) {
    super(props);
    this.state = {
      response: null,
      isLoading: false,
      models: ['mistral', 'mistral-nemo'], 
      selectedModel: 'mistral-nemo'
    };
  }

  componentDidMount() {
    this.getOrPullModel(this.state.selectedModel);
  }

  checkModelExists = async (modelName:string) => {
    try {
      await axios.post(`${this.ollamaBaseUrl}/show`, { name: modelName });
      return true; // Model exists
    } catch (error) {
      if (error instanceof AxiosError && error.response && error.response.status === 404) {
        return false; // Model doesn't exist
      }
      throw error; // Rethrow other errors
    }
  };

  pullModel = async (modelName:string) => {
    const requestBody = {
      name: modelName,
      stream: false
    };

    try {
      const response = await axios.post(`${this.ollamaBaseUrl}/pull`, requestBody);
      console.log('Model pulled successfully:', response.data);
    } catch (error) {
      console.error('Error pulling model:', (error as AxiosError).message);
    }
  };
  getOrPullModel = async (modelName:string) => {
    try {
      const modelExists = await this.checkModelExists(modelName);
      if (modelExists) {
        console.log(`Model '${modelName}' already exists.`);
      } else {
        console.log(`Model '${modelName}' not found. Pulling...`);
        await this.pullModel(modelName);
      }
    } catch (error) {
      console.error('Error:', (error as AxiosError).message);
    }
  };

  handleModelChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    this.setState({ selectedModel: event.target.value }, () => {
      this.getOrPullModel(this.state.selectedModel);
    });
  };

  sendImageToOllama = async () => {
    
    const ollamaEndpoint = "http://127.0.0.1:5000/recipe_generate" ;

    try {
      const response = await  axios.get(ollamaEndpoint);
      console.log(response.data); // Log the response data to the console
      console.log('Analyse result:', response.data);
      this.setState({ response: response.data });
      return response.data;
    } catch (error) {
      console.error('Error Process JSON:', (error as AxiosError).message);
      throw error;
    }
  };

  render(){
  return (
    <>
    <div className="app-container">
      <p className="read-the-docs">
        Warehouse UI
      </p>
      <div className="input-container">

          <button 
            onClick={this.sendImageToOllama} 
            disabled={this.state.isLoading}>
            {this.state.isLoading ? 'Processing...' : 'Analyse'}
          </button>
          <select 
            value={this.state.selectedModel} 
            onChange={this.handleModelChange}>
            {this.state.models.map((model) => (
              <option key={model} value={model}>
                {model}
              </option>
            ))}
          </select>        
      </div>    
      {this.state.response && (
        <div className="response-container">
          <h4>Response:</h4>
          <pre>{JSON.stringify(this.state.response, null, 2)}</pre>
        </div>
      )}
      </div>  
    </>
  )
}
}

export default App;
