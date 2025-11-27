jest.mock('googleapis', () => ({
  google: {
    auth: {
      OAuth2: jest.fn(() => ({
        setCredentials: jest.fn(),
        generateAuthUrl: jest.fn(() => 'https://mock-auth-url.com'),
        getToken: jest.fn(() => Promise.resolve({
          tokens: { access_token: 'mock_access_token', refresh_token: 'mock_refresh_token' }
        })),
      })),
    },
    gmail: () => ({
      users: {
        messages: {
          list: jest.fn().mockResolvedValue({
            data: { messages: [{ id: '123' }] },
          }),
          get: jest.fn().mockResolvedValue({
            data: {
              payload: {
                headers: [
                  { name: 'From', value: 'sender@example.com' },
                  { name: 'To', value: 'recipient@example.com' },
                  { name: 'Subject', value: 'Test Email' },
                ],
              },
              snippet: 'Test email body',
            },
          }),
        },
      },
    }),
  },
}));

const request = require('supertest');
const mongoose = require('mongoose');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');

const User = require('../models/User');
const Email = require('../models/Email');
const { app, shutdown } = require('../server');

let token;

describe('📧 Email Fetch E2E Tests', () => {

  beforeEach(async () => {
    await User.deleteMany({});
    await Email.deleteMany({});

    const hashedPassword = await bcrypt.hash('password123', 10);
    const user = await User.create({
      name: 'Email User',
      email: 'emailuser@example.com',
      password: hashedPassword,
      refreshToken: 'mock-refresh-token',
    });

    token = jwt.sign({ id: user._id }, process.env.JWT_SECRET, { expiresIn: '1h' });
  });

  afterAll(async () => {
    await shutdown();
    if (mongoose.connection.readyState !== 0) {
      await mongoose.disconnect();
    }
  });

  it('✅ should fetch emails from Gmail (mocked) and store them in MongoDB', async () => {
    const res = await request(app)
      .post('/api/emails/fetch')
      .set('Authorization', `Bearer ${token}`);

    expect(res.statusCode).toBe(201);
    expect(res.body).toHaveProperty('count', 1);

    const emails = await Email.find({});
    expect(emails.length).toBe(1);
    const savedEmail = emails[0];

    expect(savedEmail.sender).toBe('sender@example.com');
    expect(savedEmail.recipient).toBe('recipient@example.com');
    expect(savedEmail.subject).toBe('Test Email');
    expect(savedEmail.body).toBe('Test email body');
  });

  it('❌ should block unauthenticated requests', async () => {
    const res = await request(app).post('/api/emails/fetch');
    expect(res.statusCode).toBe(401);
  });
});
