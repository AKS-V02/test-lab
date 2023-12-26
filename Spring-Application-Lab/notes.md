***origin branch***
git remote add origin https://github.com/AKS-V02/test-lab.git
git branch -M main
git push -u origin main

***to start the app use below cmd***
mvn package(provided maven is installed or use ./mvnw in place of mvn)
mvn spring-boot:run(this should be run where pom file is) 
or java -jar <jar file>
================================================================
**type of application properties in Spring Boot**
core, web, security, data, Actuator, intigration, DevTools, Testing

===================================================================


***Scope of a bean***(we can set the scope of a bean on class level check the TrackCoach class)
**singleton(default)**= only single shared instance of bean class is created
**prototype**= create new bean instance for each container request
**request**= Scoped to an http web request.only used for web app
**session**= Scoped to an http web session.only used for web app
**global-session**= Scoped to an http global web session.only used for web app

====================================================================

***Bean life Cycle***check the CreacketCoach class
Container started --> Bean Instantiated --> Dependencies Injected --> Internal Spring Processing --> My Coustom Init Method 
--> Bean is ready for use || Container is Shutdown --> 
my Custom Destroy Method --> stop

**Special Note about Prototype Scope - Destroy Lifecycle Method and Lazy Init**
**Prototype Beans and Destroy Lifecycle**
There is a subtle point you need to be aware of with "prototype" scoped beans.

For "prototype" scoped beans, Spring does not call the destroy method. Gasp!

---

**In contrast to the other scopes, Spring does not manage the complete lifecycle of a prototype bean**: the container instantiates, configures, and otherwise assembles a prototype object, and hands it to the client, with no further record of that prototype instance.

Thus, although initialization lifecycle callback methods are called on all objects regardless of scope, in the case of prototypes, configured destruction lifecycle callbacks are not called. The client code must clean up prototype-scoped objects and release expensive resources that the prototype bean(s) are holding.

=======================================================================


