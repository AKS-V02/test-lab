package com.my.lab;

import java.io.BufferedOutputStream;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.time.LocalDateTime;
import java.time.ZoneOffset;
import java.time.format.DateTimeFormatter;

import org.springframework.http.HttpEntity;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.http.client.SimpleClientHttpRequestFactory;
import org.springframework.web.client.HttpClientErrorException;
import org.springframework.web.client.HttpServerErrorException;
import org.springframework.web.client.RestTemplate;

public class RestApiInvoker {
    
    private static RestTemplate restTemplate;

    private static String S3_UPLOAD_AWS_ACCESS_KEY = "";
    private static String S3_UPLOAD_AWS_SECRET_KEY = "";

    public static RestTemplate getRestTemplate() {
        if(restTemplate==null){
            restTemplate = new RestTemplate();
            SimpleClientHttpRequestFactory clientHttpRequestFactory
                      = (SimpleClientHttpRequestFactory) restTemplate.getRequestFactory();
            clientHttpRequestFactory.setConnectTimeout(30000); 
            clientHttpRequestFactory.setReadTimeout(30000);         
        }
        return restTemplate;
    }
    

    public static ResponseEntity<byte[]> invoke(String url, HttpMethod method, HttpEntity<?> req){
        ResponseEntity<byte[]> resp = null;
        try {
            resp = getRestTemplate().exchange(url, method, req, byte[].class);
        } catch (HttpClientErrorException e) {
            System.out.println("HttpClientErrorException# status code"+e.getStatusCode()+" respbody: "+e.getResponseBodyAsString());
        } catch (HttpServerErrorException e) {
            System.out.println("HttpServerErrorException# status code: "+e.getStatusCode()+" respbody: "+e.getResponseBodyAsString());
        } catch (Exception e) {
            System.out.println("Error: "+e.getMessage());
        }
        return resp;
    }

    public static void callS3Api(){
        
    }


     // Example AWS region
    private static final String REGION = "ap-south-1";

    // <localstack_endpoint>/<bucket_name>
    // For real S3, use <bucket-name>.s3.<aws_region>.amazonaws.com
    private static final String BUCKET_ENDPOINT = "https://s3-rest-api-test-dev.s3.ap-south-1.amazonaws.com";

    // key of the object to save
    private static final String OBJECT_NAME = "public/object.json";

    public static void main(String[] args) throws IOException {
        // File in the example is in the current dir
        Path file = Paths.get(OBJECT_NAME);
        
        String type;
        long fileSize;
        try {
            // Probe content type and size
            type = Files.probeContentType(file);
            fileSize = Files.size(file);
        } catch (IOException e) {
            System.err.println("Cannot analyze file " + OBJECT_NAME + "!");
            e.printStackTrace();
            return;
        }

        URL url = new URL(BUCKET_ENDPOINT + "/" + OBJECT_NAME);
        HttpURLConnection httpConnection;

        try {
            // Connect to S3
            httpConnection = (HttpURLConnection) url.openConnection();
        } catch (IOException e) {
            System.err.println("Cannot connect to bucket " + BUCKET_ENDPOINT + "!");
            e.printStackTrace();
            return;
        }

        httpConnection.setRequestMethod("PUT");
        httpConnection.setRequestProperty("Host", BUCKET_ENDPOINT);
        httpConnection.setRequestProperty("Content-Type", type);
        httpConnection.setRequestProperty("Content-Length", String.valueOf(fileSize));

        String datetime = LocalDateTime.now().atOffset(ZoneOffset.UTC).format(DateTimeFormatter.ofPattern("yyyyMMdd'T'HHmmssZ"));

        // Example AWS headers
        // More: https://docs.aws.amazon.com/AmazonS3/latest/API/API_PutObject.html
        httpConnection.setRequestProperty("x-amz-date", datetime);
        // httpConnection.setRequestProperty("x-amz-server-side-encryption", "AES256");
        // httpConnection.setRequestProperty("x-amz-tagging", "description=triangle");

        // Authorization (IAM authentication)
        // You must sign the request manually
        // Reference: https://docs.aws.amazon.com/AmazonS3/latest/API/sigv4-auth-using-authorization-header.html
        httpConnection.setRequestProperty("Authorization", "AWS4-HMAC-SHA256 " +
                                                            // Credential=<access_key_id>/<date_in_yyyyMMdd_format>/<aws_region>/<aws_service>/aws4_request
                                                           "Credential="+S3_UPLOAD_AWS_ACCESS_KEY+"/" + datetime.substring(0, datetime.indexOf('T')) + "/" + REGION + "/s3/aws4_request," +
                                                            // Headers used in sign process
                                                           "SignedHeaders=host;content-type;x-amz-date;content-length," +
                                                            // 256-bit signature (you must calculate it manually)
                                                            // this is an example
                                                           "Signature=fe5f80f77d5fa3beca038a248ff027d0445342fe2855ddc963176630326f1024");

        // Write the object to S3
        // and read the response, if failure
        httpConnection.setDoInput(true);
        httpConnection.setDoOutput(true);

        try(BufferedOutputStream outstream = new BufferedOutputStream(httpConnection.getOutputStream())) {
            // Write the file to S3
            Files.copy(file, outstream);
        } catch(IOException e) {
            System.err.println("Cannot send object to bucket " + BUCKET_ENDPOINT + "!");
            e.printStackTrace();
            httpConnection.disconnect();
            return;
        }

        int responseStatus = httpConnection.getResponseCode();

        if (responseStatus == 200) {
            // Success
            System.out.println(OBJECT_NAME + " uploaded successfully to bucket " + BUCKET_ENDPOINT + "!");
        } else {
            // Failure
            System.out.println(OBJECT_NAME + " upload failed!");
            System.out.println("Status " + responseStatus);
            System.out.println("Response:");
            System.out.println();
            try(BufferedReader reader = new BufferedReader(new InputStreamReader(httpConnection.getErrorStream()))) {
                String line;
                while ((line = reader.readLine()) != null) {
                    System.out.println(line);
                }
            } catch(IOException e) {
                System.err.println("Cannot read from " + BUCKET_ENDPOINT + "!");
                e.printStackTrace();
            }
        }

        // Close the connection to S3
        httpConnection.disconnect();
    }

}
