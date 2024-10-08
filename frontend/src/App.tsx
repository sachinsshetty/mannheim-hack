import { Component } from 'react';
import ReactDOMServer from 'react-dom/server';
import axios from 'axios';
import { AxiosError } from 'axios';
import './App.css'

interface AppState {
  response: any;
  isLoading: boolean;
  models: string[]; 
  selectedModel: string; 
  responseJson: string;

}

function cleanJsonString(inputString: string) {
  const prefix = "```json";
  const suffix = "```";
  // Check if the string starts with the prefix and ends with the suffix
  if (inputString.startsWith(prefix) && inputString.endsWith(suffix)) {
      // Remove the prefix and suffix
      const cleanedString = inputString.slice(prefix.length, -suffix.length).trim();
      const jsonObject = JSON.parse(cleanedString);
      return jsonObject;
  } else {
      return inputString; // Return the original string if conditions are not met
  }
}

class App extends Component<{}, AppState> {
  ollamaBaseUrl = import.meta.env.VITE_OLLAMA_BASE_URL;
  constructor(props:{}) {
    super(props);
    this.state = {
      response: null,
      isLoading: false,
      models: ['mistral', 'mistral-nemo'], 
      selectedModel: 'mistral-nemo',
      responseJson: '',
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
    
    const modelName = this.state.selectedModel;
    
    //const ollamaEndpoint = "http://localhost:5000/recipe_generate?model_name=${modelName}" ;
    const ollamaEndpoint = 'http://localhost:5000/recipe_generate/' + modelName;
    console.log(ollamaEndpoint);

    try {
      const response = await  axios.get(ollamaEndpoint);
      //console.log('Analyse result:', response.data);
      const respone_data = cleanJsonString(response.data);
      console.log(respone_data);


      this.setState({ response: respone_data });
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
        Supervisor Agent
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
          <h4>Smart Bundles:</h4>
          <textarea value={this.state.response} readOnly style={{ width: '600px', height: '600px' }}/>
        </div>
      )}
      </div>  
    </>
  )
}
}

export default App;
