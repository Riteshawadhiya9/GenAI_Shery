# GenAI_Shery

A generative AI-powered chatbot application designed to provide intelligent conversations and interactive chat experiences.

## 📋 Project Overview

GenAI_Shery is a Python-based chatbot system that combines AI models with a user-friendly interface. The project implements multiple chat models and provides both CLI and UI-based interactions for seamless user experience.

## 📁 Project Structure

```
GenAI_Shery/
├── chatmodels/              # Chat model implementations
│   ├── chat.py             # Core chat functionality
│   ├── chatbot.py          # Chatbot logic and orchestration
│   └── UIchatbot.py        # UI-based chatbot interface
├── CineSage/               # Data models and validation
│   └── pydantic.py         # Pydantic models for data validation
├── requirements.txt        # Python dependencies
└── README.md              # Project documentation
```

## ✨ Features

- **Multi-model Chat Support**: Flexible chat implementations for different use cases
- **User Interface**: Interactive UI chatbot for enhanced user experience
- **Data Validation**: Pydantic models for robust data handling
- **CLI & GUI**: Support for both command-line and graphical interfaces

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/GenAI_Shery.git
cd GenAI_Shery
```

2. Create a virtual environment:
```bash
python -m venv .venv
```

3. Activate the virtual environment:

**On Windows:**
```bash
.venv\Scripts\activate
```

**On macOS/Linux:**
```bash
source .venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

## 📦 Dependencies

All required dependencies are listed in `requirements.txt`. Install them using:
```bash
pip install -r requirements.txt
```

## 🎯 Usage

### Using the Chatbot

```python
from chatmodels import chatbot

# Initialize the chatbot
bot = chatbot.Chatbot()

# Start conversation
response = bot.chat("Your message here")
print(response)
```

### Using the UI Chatbot

```python
from chatmodels import UIchatbot

# Launch the UI interface
UIchatbot.run()
```

## 🏗️ Architecture

- **chatmodels/**: Contains the core chat engine and bot implementations
- **CineSage/**: Handles data validation and pydantic schemas

## 🛠️ Development

### Adding New Features

1. Create a new branch for your feature
2. Make your changes
3. Test thoroughly
4. Submit a pull request

### Running Tests

```bash
# Run your test suite
pytest
```

## 📝 Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## ⚠️ Security

Please never commit sensitive information such as:
- API keys
- Environment variables (.env files)
- Credentials
- Secrets

These are automatically excluded by `.gitignore`.

## 📄 License

This project is open source. Please see the LICENSE file for more details (if applicable).

## 👤 Author

**Ritesh Awadhiya**

## 🤝 Support

For support, email your-email@example.com or open an issue in the repository.

## 🗺️ Roadmap

- [ ] Multi-language support
- [ ] Advanced NLP features
- [ ] Database integration
- [ ] API endpoints
- [ ] Deployment to cloud

## 📚 References

- Python Documentation: https://docs.python.org/
- Pydantic: https://pydantic-docs.helpmanual.io/
- LangChain: https://python.langchain.com/
