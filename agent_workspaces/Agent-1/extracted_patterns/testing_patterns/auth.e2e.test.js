const request = require('supertest');
const mongoose = require('mongoose');
const User = require('../models/User');
const bcrypt = require('bcryptjs');

const { app } = require('../server');

describe('🔐 Auth E2E Tests', () => {

  beforeEach(async () => {
    while (mongoose.connection.readyState !== 1) {
      await new Promise(resolve => setTimeout(resolve, 100));
    }
    await User.deleteMany({});
  });

  afterAll(async () => {
    await mongoose.disconnect(); // or await shutdown();
  });

  it('✅ should register a user successfully', async () => {
    const res = await request(app)
      .post('/api/auth/register')
      .send({
        name: 'Test User',
        email: 'test@example.com',
        password: 'password123',
      });

    expect(res.statusCode).toBe(201);
    expect(res.body).toHaveProperty('accessToken');
    expect(res.body.user.email).toBe('test@example.com');

    const user = await User.findOne({ email: 'test@example.com' });
    expect(user).not.toBeNull();
  });

  it('✅ should login an existing user and return a token', async () => {
    const hashedPassword = await bcrypt.hash('password123', 10);
    await User.create({
      name: 'Test User',
      email: 'test@example.com',
      password: hashedPassword,
    });

    const res = await request(app)
      .post('/api/auth/login')
      .send({
        email: 'test@example.com',
        password: 'password123',
      });

    expect(res.statusCode).toBe(200);
    expect(res.body).toHaveProperty('accessToken');
    expect(res.body.user.email).toBe('test@example.com');
  });

  it('❌ should block access to protected route without token', async () => {
    const res = await request(app).post('/api/emails/fetch');
    
    expect(res.statusCode).toBe(401);
    expect(res.body.msg).toMatch(/no token/i);
  });

});
