const titleElement = document.getElementById("title");
titleElement.append(" Testing");
document.write("hello world")



const response = require('cfn-response');
const aws = require('aws-sdk');
const identity = new aws.CognitoIdentityServiceProvider();
exports.handler = (event, context, callback) => {  
    if (event.RequestType == 'Delete') {    
        response.send(event, context, response.SUCCESS, {});  
    }  if (event.RequestType == 'Update' || event.RequestType == 'Create') {    
        const params = {    ClientId: event.ResourceProperties.clientId,      
                            UserPoolId: event.ResourceProperties.userpoolId,    
                        };    
        identity.describeUserPoolClient(params).promise().then((res) => {        
            response.send(event, context, response.SUCCESS, { appSecret: res.UserPoolClient.ClientSecret });      
        }).catch((err) => {   
            response.send(event, context, response.FAILED, { err });      
        });  
    }
};


const response = require('cfn-response');
const aws = require('aws-sdk');
exports.handler = async function (event, context) {  
    const physicalResourceId =    event.RequestType === 'Update' ? 
                                    event.PhysicalResourceId : 
                                        `${event.LogicalResourceId}-${event.ResourceProperties.userpoolId}`;  
    try {    
        const userPoolId = event.ResourceProperties.userpoolId;    
        const { lambdaConfig } = event.ResourceProperties;    
        const config = {};    
        const cognitoClient = new aws.CognitoIdentityServiceProvider();
        const userPoolConfig = await cognitoClient.describeUserPool({ UserPoolId: userPoolId }).promise();    
        const userPoolParams = userPoolConfig.UserPool;    
        // update userPool params    
        const updateUserPoolConfig = {      
            UserPoolId: userPoolParams.Id,      
            Policies: userPoolParams.Policies,      
            SmsVerificationMessage: userPoolParams.SmsVerificationMessage,      
            AccountRecoverySetting: userPoolParams.AccountRecoverySetting,      
            AdminCreateUserConfig: userPoolParams.AdminCreateUserConfig,      
            AutoVerifiedAttributes: userPoolParams.AutoVerifiedAttributes,      
            EmailConfiguration: userPoolParams.EmailConfiguration,      
            EmailVerificationMessage: userPoolParams.EmailVerificationMessage,      
            EmailVerificationSubject: userPoolParams.EmailVerificationSubject,      
            VerificationMessageTemplate: userPoolParams.VerificationMessageTemplate,      
            SmsAuthenticationMessage: userPoolParams.SmsAuthenticationMessage,      
            MfaConfiguration: userPoolParams.MfaConfiguration,      
            DeviceConfiguration: userPoolParams.DeviceConfiguration,      
            SmsConfiguration: userPoolParams.SmsConfiguration,      
            UserPoolTags: userPoolParams.UserPoolTags,      
            UserPoolAddOns: userPoolParams.UserPoolAddOns,    
        };    
        // removing undefined keys    
        Object.keys(updateUserPoolConfig).forEach((key) => 
            updateUserPoolConfig[key] === undefined && delete updateUserPoolConfig[key]);    
            /* removing UnusedAccountValidityDays as deprecated    
            InvalidParameterException: Please use TemporaryPasswordValidityDays in PasswordPolicy instead of 
            UnusedAccountValidityDays    */    
        if (updateUserPoolConfig.AdminCreateUserConfig 
            && updateUserPoolConfig.AdminCreateUserConfig.UnusedAccountValidityDays) {      
                delete updateUserPoolConfig.AdminCreateUserConfig.UnusedAccountValidityDays;    
            }    
        lambdaConfig.forEach((lambda) => (
            config[`${lambda.triggerType}`] = lambda.lambdaFunctionArn
            ));    
        if (event.RequestType === 'Delete') {      
            try {        
                updateUserPoolConfig.LambdaConfig = {};        
                console.log(`${event.RequestType}:`, JSON.stringify(updateUserPoolConfig));        
                const result = await cognitoClient.updateUserPool(updateUserPoolConfig).promise();        
                console.log(`delete response data ${JSON.stringify(result)}`);        
                await response.send(event, context, response.SUCCESS, {}, physicalResourceId);      
            } catch (err) {        
                console.log(err.stack);        
                await response.send(event, context, response.FAILED, { err }, physicalResourceId);      
            }    
        }    
        if (event.RequestType === 'Update' || event.RequestType === 'Create') {      
            updateUserPoolConfig.LambdaConfig = config;      
            try {        
                const result = await cognitoClient.updateUserPool(updateUserPoolConfig).promise();        
                console.log(`createOrUpdate response data ${JSON.stringify(result)}`);        
                await response.send(event, context, response.SUCCESS, {}, physicalResourceId);      
            } catch (err) {        
                console.log(err.stack);        
                await response.send(event, context, response.FAILED, { err }, physicalResourceId);      
            }    
        }  
    } catch (err) {    
            console.log(err.stack);    
            await response.send(event, context, response.FAILED, { err }, physicalResourceId);  
    }
};




const response = require('cfn-response');
const AWS = require('aws-sdk');
exports.handler = (event, context) => {
	if (event.RequestType == 'Delete') {
		response.send(event, context, response.SUCCESS, { message: 'Request type delete' });
	}
    if (event.RequestType == 'Create' || event.RequestType == 'Update') {
        let { identityPoolId, appClientID, appClientIDWeb, userPoolId, region } = event.ResourceProperties;
        try {
            const cognitoidentity = new AWS.CognitoIdentity();
            let params = {
                IdentityPoolId: identityPoolId,
                Roles: {
                        authenticated: event.ResourceProperties.AuthRoleArn,
                        unauthenticated: event.ResourceProperties.UnauthRoleArn,
                        },
                RoleMappings: {},
                };
            if (appClientIDWeb) {
                params.RoleMappings[`cognito-idp.${region}.amazonaws.com/${userPoolId}:${appClientIDWeb}`] = {
                        Type: 'Token',
                        AmbiguousRoleResolution: 'AuthenticatedRole',
                    };
            }
            if (appClientID) {
                params.RoleMappings[`cognito-idp.${region}.amazonaws.com/${userPoolId}:${appClientID}`] = {
                    Type: 'Token',
                        AmbiguousRoleResolution: 'AuthenticatedRole',
                    };
            }
            cognitoidentity.setIdentityPoolRoles(params).promise();
            response.send(event, context, response.SUCCESS, { message: 'Successfully updated identity pool.' });
        } catch (err) {
            response.send(event, context, response.FAILED, { message: 'Error updating identity pool' });
        }
    }
};
                




