const mongoose = require('mongoose');
const { shutdown } = require('../server');

module.exports = async () => {
  console.log('🧹 Global teardown started...');

  try {
    await shutdown({ exit: false }); // ✅ DON'T EXIT during test cleanup

    if (mongoose.connection.readyState !== 0) {
      await mongoose.disconnect();
      console.log('✅ Mongoose disconnected.');
    }

    if (global.__MONGO_SERVER__) {
      await global.__MONGO_SERVER__.stop({ doCleanup: true, force: true });
      console.log('✅ In-memory MongoDB stopped.');
    }

    console.log('✅ Global teardown complete.');
  } catch (error) {
    console.error('❌ Error during global teardown:', error);
  }
};
