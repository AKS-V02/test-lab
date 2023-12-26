package com.my.lab;

import java.io.PrintStream;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.time.Instant;
import java.time.LocalDate;
import java.time.Month;
import java.time.ZoneId;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Calendar;
import java.util.HashSet;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.Optional;
import java.util.Set;
import java.util.StringJoiner;
import java.util.TimeZone;
import java.util.function.Consumer;
import java.util.stream.Collectors;
import java.util.stream.IntStream;
import java.util.stream.Stream;
import java.util.zip.ZipFile;

import javax.script.ScriptEngine;

/**
 * Hello world!
 *
 */
public class App 
{
    public static void main( String[] args )
    {
        System.out.println( "Hello World!" );

        List<Student> elist = List
                    .of(new Student("Stenny", 24),
                    new Student("Rucha", 22),
                    new Student("Vihaan", 21),
                    new Student("Stenny", 22)    
                    );
        Map<String, Integer> map = elist.stream()
        .collect(Collectors.toMap(Student::getName, 
                        Student::getAge,
                        (oldV, newV)->oldV));
        System.out.println(map);
        
        // elist.forEach(consumerWrappre(num->System.out.println(""),ArithmeticException.class));

        // String fileName = "c://Sample.txt";

        // try(Stream<String> stream = Files.lines(Paths.get(fileName))){
        //     stream.forEach(System.out::println);
        // } catch (Exception e) {
        //     // TODO: handle exception
        // }

        StringJoiner jr1 = new StringJoiner("delimeter", "pre", "suf");
        jr1.merge(jr1);

        Set<Integer> intSet = new HashSet<>();
        intSet.add(47);
        intSet.forEach(System.out::println);

        LocalDate date = LocalDate.of(2019, Month.MARCH, 30);
        LocalDate date2 = LocalDate.ofYearDay(2020, 255);
        LanguageService ll = message -> System.out.println("ff"+message);
        ll.showMassage("ff");

        // Calculator sum = (int sum)-> a+b;
        // int a = sum.add(4,5);


        double radiu = 4.55;
        Circle circle = (double radius)->3.14*radius*radius;
        circle.calculateArea(radiu);

        List<String> data = Arrays.asList("ss","wws","rr");
        List<String> sortedData = data.stream()
                .sorted((s1,s2)->s1.compareTo(s2)).collect(Collectors.toList());
        System.out.println("sorted "+sortedData);
        List<String> sortedData2 = data.stream()
                .sorted(String::compareTo).collect(Collectors.toList());
        System.out.println("sorted2 "+sortedData2);
        
        
        App x = new App();
        myInte obj = x.new Myclass();
        obj.name();

        Optional<Integer> op = Optional.ofNullable(null);

        // double dd = data.stream().collect(Collectors.averagingInt(null));

        Stream<Student> st = elist.stream().filter(stu->stu.getName().equalsIgnoreCase("kk"));

        final Calendar calendar = new Calendar.Builder().setInstant(Instant.now().toEpochMilli())
                                .setTimeZone(TimeZone.getTimeZone(ZoneId.systemDefault())).setLocale(Locale.getDefault()).build();

        System.out.println("Time "+ Instant.ofEpochMilli(Instant.now().toEpochMilli()));

        List<Integer> integersList = IntStream.range(1, 10).boxed()
            .collect(Collectors.toCollection(ArrayList::new));
        System.out.println("intiger list"+integersList);
    }

    public void printEntries(PrintStream stream, String zip){
        try (ZipFile zipFile = new ZipFile(zip)){
            zipFile.stream().forEach(stream::println);
        } catch (Exception e) {
            // TODO: handle exception
        }
    }

    interface myInte{
        default void name() {
            System.out.println("myInterface");
        }
    }

    class Myclass implements myInte{
        public void name(){
            System.out.println("my class");
        }
    }
    
    
    
    @FunctionalInterface
    public interface Circle{
        double calculateArea(double radius);
    }

    // @FunctionalInterface
    // public interface Calculator{
    //     int add(int a, int b);
    //     int multiply(int a, int b);
    // }
    interface LanguageService{
        void showMassage(String message);
    }

    static <T,E extends Exception> Consumer<T> 
                        consumerWrappre(Consumer<T> consumer, Class<E> clazz){
                            return num ->{
                                try {
                                    consumer.accept(num);
                                } catch (Exception e) {
                                    E exCast = clazz.cast(e);
                                    System.err.println("exception "+exCast.getMessage());
                                }
                            };
    }
}
