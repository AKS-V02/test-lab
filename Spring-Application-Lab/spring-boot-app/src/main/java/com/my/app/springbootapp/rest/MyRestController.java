package com.my.app.springbootapp.rest;

import org.springframework.web.bind.annotation.RestController;

import com.my.app.springbootapp.trainning.Coach;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.web.bind.annotation.GetMapping;
// import org.springframework.web.bind.annotation.RequestParam;


@RestController
public class MyRestController {
    
    // rest endpoint mapping to the methods
    @GetMapping(value="/")
    public String getHellow() {
        return "Hellow";
    }

    @GetMapping(value="/new")
    public String getNewPath() {
        return "new path for me";
    }

    //====example for accessing the values or env variables form application. properties file

    // properties form aplication.properties file
    @Value("${my.first.name}")
    private String firstName;

    @Value("${my.last.name}")
    private String lastName;
    
    @GetMapping(value="/myname")
    public String getMethodName() {
        return "My name: "+firstName+" "+lastName;
    }

    //======== example for dependency injection
    
    // define a private property 
    // @Autowired // for field injection(not recomended as it is very hard to do the junit test for this)
    private Coach newCoach;

    //define a constuctor for dependency injection(constuctor injection)
    // @Autowired // this anotation teals spring to inject dependency and if there is ony one contructor then it is optional
    // public MyRestController(Coach theCoach){
    //     this.newCoach = theCoach;
    // }

    //define a set method for setter injection(partial dependency injection)
    // @Autowired // method name could be any name
    // public void setCoach(Coach theCoach){
    //     this.newCoach = theCoach;
    // }


    //==========qualifier example 
    //qualifier is used for specifying the bean class incase of multiple bean class, 
    //name is same as the class firat letter small
    //primary anotation can also be used at class level to specify specific class check, CricketCoach class
    //Qualifier annotation has higher priority than Primary Annotation, Qualifier can override Primary bean selection
    // @Autowired 
    // public MyRestController(@Qualifier("cricketCoach") Coach theCoach){
    //     System.out.println(" inside Constructor "+ getClass().getSimpleName());  
    //     this.newCoach = theCoach;
    // }



    @GetMapping(value="/getDailyWorkOut")
    public String getDailyWorkOut() {
        return newCoach.getDailyWorkOut();
    }

    // Scope example

    // private Coach nextCoach;
    
    // @Autowired 
    // public MyRestController(@Qualifier("trackCoach") Coach theCoach,
    //                         @Qualifier("trackCoach") Coach nextCoach){  
    //     this.newCoach = theCoach;
    //     this.nextCoach = nextCoach;
    // }

    // as for singleton scope only one instance is 
    //created on a memory location so reference always same
    // @GetMapping(value="/checkScope")
    // public String checkScope() {
    //     if(newCoach==nextCoach)
    //         return "singleton";
    //     else
    //         return "prototype";
    // }



    // Java configuration bean creation example check the JavaBeanConfiguration class
    @Autowired 
    public MyRestController(@Qualifier("newSwimCoach") Coach theCoach){
        System.out.println(" inside Constructor "+ getClass().getSimpleName());  
        this.newCoach = theCoach;
    }
    
    
}
