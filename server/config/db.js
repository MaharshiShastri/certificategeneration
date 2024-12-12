const mongoose = require('mongoose');

const connectionDB = async() => {
    try{
        await mongoose.connect(process.env.MONGO_URI, {
            userNewURLParser: true,
            useUnifiedTopology: true,
        });
        console.log('MongoDDB connected...');
    }
    catch(err){
        console.error(err.message);
        process.exit(1);
    }
};

module.exports = connectDB;
