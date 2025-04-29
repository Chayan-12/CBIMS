const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const dotenv = require('dotenv');
const jwt = require('jsonwebtoken');

// Load environment variables
dotenv.config();

const app = express();

// Middlewares
app.use(cors());
app.use(express.json());

// MongoDB Connection
mongoose.connect(process.env.MONGO_URI, {
  useNewUrlParser: true,
  useUnifiedTopology: true,
})
.then(() => console.log('✅ Connected to MongoDB'))
.catch((err) => console.error('❌ MongoDB connection error:', err));

// Threat Schema
const ThreatSchema = new mongoose.Schema({
  message: String,
  detectedAt: { type: Date, default: Date.now }
});

const Threat = mongoose.model('Threat', ThreatSchema);

// Simple Auth Middleware (JWT)
const authenticate = (req, res, next) => {
  const token = req.header('Authorization')?.split(' ')[1];
  if (!token) return res.status(401).send('Access Denied');

  try {
    const verified = jwt.verify(token, process.env.JWT_SECRET);
    req.user = verified;
    next();
  } catch (err) {
    res.status(400).send('Invalid Token');
  }
};

// Routes
app.get('/', (req, res) => {
  res.send('🛡️ Cybersecurity Detection System Backend Running');
});

// Get all threats (secured route)
app.get('/api/threats', authenticate, async (req, res) => {
  try {
    const threats = await Threat.find().sort({ detectedAt: -1 });
    res.json(threats);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
});

// Add a new threat (for testing)
app.post('/api/threats', authenticate, async (req, res) => {
  const { message } = req.body;
  const newThreat = new Threat({ message });

  try {
    const savedThreat = await newThreat.save();
    res.status(201).json(savedThreat);
  } catch (err) {
    res.status(400).json({ message: err.message });
  }
});

// User login (temporary token generator for testing)
app.post('/api/login', (req, res) => {
  const { username } = req.body;
  // Normally validate username and password here
  const token = jwt.sign({ username }, process.env.JWT_SECRET, { expiresIn: '1h' });
  res.json({ token });
});

// Start Server
const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log(`🚀 Server running on port ${PORT}`));
