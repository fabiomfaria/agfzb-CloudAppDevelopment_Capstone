/**
 * Get all databases
 */

const Cloudant = require('@cloudant/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');

function main(params) {

    const cloudant = Cloudant({
        url: params.COUCH_URL,
        plugins: { iamauth: { iamApiKey: params.IAM_API_KEY } }
    });

    let dbList = getDbs(cloudant);
    return { dbs: dbList };
}

function getDbs(cloudant) {
    cloudant.getAllDbs().then((body) => {
        body.forEach((db) => {
            dbList.push(db);
        });
    }).catch((err) => { console.log(err); });
}

