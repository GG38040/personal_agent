# Personal Email & Calendar Assistant

A Python-based personal assistant that helps manage your Gmail and Google Calendar using natural language commands and OpenAI's GPT model.

## 🌟 Features

- **Email Management**
  - Read recent emails
  - Send emails
  - Search inbox
- **Calendar Integration**
  - Add events
  - List upcoming events
  - Schedule meetings
- **Natural Language Processing**
  - Conversational interface
  - Context-aware responses
  - Smart command parsing

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Google Account
- OpenAI API Key

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/personal-agent.git
cd personal-agent
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up Google Cloud Project**
   - Visit [Google Cloud Console](https://console.cloud.google.com)
   - Create a new project
   - Enable Gmail and Calendar APIs
   - Configure OAuth consent screen
   - Create OAuth 2.0 credentials
   - Download `credentials.json`

4. **Configure environment**
   - Create `.env` file:
```plaintext
OPENAI_API_KEY=your_api_key_here
```

## 📁 Project Structure
```
personal_agent/
├── agent.py              # OpenAI integration
├── gmail_integration.py  # Gmail API handling
├── calendar_integration.py # Calendar API handling
├── google_auth.py       # Google authentication
├── main.py             # Main application
├── config.py           # Configuration
├── prompts/
│   └── system_prompt.txt # AI system instructions
├── memory/
│   ├── memory.py      # Conversation memory
│   └── chat.json      # Chat history
└── requirements.txt    # Dependencies
```

## 🛠️ Configuration

1. **Google API Setup**
   - Place `credentials.json` in project root
   - First run will prompt for Google authentication
   - Tokens are saved for future use

2. **OpenAI Configuration**
   - Add your OpenAI API key to `.env`
   - Modify `system_prompt.txt` for custom behavior

## 📝 Usage

Start the assistant:
```bash
python main.py
```

### Example Commands:
```plaintext
list emails
send email|recipient@example.com|Subject|Message
add event|Meeting with Team|2024-06-05|14:30
list events
```

## 🔒 Security
- OAuth 2.0 for Google API authentication
- Environment variables for sensitive keys
- Local storage of authentication tokens
- No permanent storage of email content

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments
- OpenAI GPT for natural language processing
- Google APIs for email and calendar integration
- Python community for amazing libraries

## 🔧 Troubleshooting

### Common Issues:
1. **Authentication Errors**
   - Delete `token.json` and reauthorize
   - Verify Google Cloud Console settings
   - Check API enablement

2. **API Limits**
   - Monitor Google API quotas
   - Implement rate limiting if needed

## 📚 Documentation
For detailed documentation on each component:
- [Gmail API Documentation](https://developers.google.com/gmail/api)
- [Google Calendar API Documentation](https://developers.google.com/calendar)
- [OpenAI API Documentation](https://platform.openai.com/docs/api-reference)