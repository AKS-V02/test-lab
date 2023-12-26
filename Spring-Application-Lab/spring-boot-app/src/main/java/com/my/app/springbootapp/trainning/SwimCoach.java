package com.my.app.springbootapp.trainning;

public class SwimCoach implements Coach{

    public SwimCoach(){
        System.out.println(" inside Constructor "+ getClass().getSimpleName());
    }

    @Override
    public String getDailyWorkOut() {
        return "Practice Swiming";
    }
    
}
