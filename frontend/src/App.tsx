import { Component, ChangeEvent } from 'react';
import axios from 'axios';
import { AxiosError } from 'axios';
import './App.css'
import TextField from '@mui/material/TextField';

interface AppState {
  response: any;
  prompt: string;
  json_api: string;
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
      prompt: '1. State the name of the food item.' +
        '2. Mention the expiration date to raise awareness about freshness.' +
        '3. Describe the best storage practices to prolong shelf life.'+
        '4. List creative ways to use the food item to encourage consumption before it spoils.'+
        '5. Provide actionable tips for minimizing waste, such as recipes or preservation methods.'+
        'JSON DATA = {}',
      json_api: '[{"id":"8376291","name":"Organic Cherry Tomatoes","expiresAt":"2024-09-23","price":2.99,"weight":"250g","packagingUnit":"punnet","available":48},{"id":"5728364","name":"Sweet Potatoes","expiresAt":"2024-10-15","price":1.79,"weight":"1kg","packagingUnit":"bag","available":23},{"id":"9126483","name":"Broccoli Florets","expiresAt":"2024-09-18","price":2.49,"weight":"400g","packagingUnit":"bag","available":17},{"id":"4537281","name":"Red Bell Peppers","expiresAt":"2024-12-02","price":1.29,"weight":"500g","packagingUnit":"each","available":62},{"id":"1928374","name":"Baby Spinach","expiresAt":"2024-09-27","price":3.99,"weight":"150g","packagingUnit":"bag","available":8},{"id":"6273849","name":"White Onions","expiresAt":"2025-01-10","price":0.79,"weight":"1kg","packagingUnit":"bag","available":41}]',
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

  handlePromptChange = (event: ChangeEvent<HTMLInputElement>) => {
    this.setState({ prompt: event.target.value });
  };

  handleJsonAPI = (event: ChangeEvent<HTMLInputElement>) => {
    this.setState({ json_api: event.target.value });
  };


  handleModelChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    this.setState({ selectedModel: event.target.value }, () => {
      this.getOrPullModel(this.state.selectedModel);
    });
  };

  sendImageToOllama = async () => {
    //if (!this.state.base64StringImage) return;
    
    const requestBody = {
      model: 'mistral-nemo',
      messages: [
        {
          role: 'user',
          content: this.state.prompt + ' ' +  this.state.json_api
        }
      ],
      stream: false
    };

    const ollamaEndpoint = this.ollamaBaseUrl + '/chat';

    try {
      const response = await axios.post(ollamaEndpoint, requestBody);
      console.log("Prompt - ", this.state.prompt);
      console.log('Analyse result:', response.data.message.content);
      this.setState({ response: response.data.message.content });
      return response.data.message.content;
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
          <TextField
            value={this.state.prompt}
            onChange={this.handlePromptChange}
            placeholder="Enter your prompt here..."
            fullWidth
          />
          <TextField
            value={this.state.json_api}
            onChange={this.handleJsonAPI}
            placeholder="Enter your JSON here..."
            fullWidth
          />

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
          {this.state.uploadedImage && (
              <img 
              src={this.state.uploadedImage} 
              alt="Uploaded" 
              width="100" height="100" />
            )}
        </div>
      )}
      </div>  
    </>
  )
}
}

export default App;
