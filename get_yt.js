const https = require('https'); 
const ids = ['Syk0rwciis4', 'umixCEEZjbk', 'RPZbRVCAImo']; 
ids.forEach(id => { 
    https.get(`https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v=${id}&format=json`, res => { 
        let data = ''; 
        res.on('data', chunk => data+=chunk); 
        res.on('end', () => console.log(`${id}: ${JSON.parse(data).title}`)); 
    }); 
});
