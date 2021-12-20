package com.mail;

import java.io.*;
import java.util.*;

public class FileAuthenticator {

    public static void main(String[] args) throws IOException {
        BufferedReader emailFileReader = new BufferedReader(new FileReader("inbox.txt"));
        BufferedReader csvFileReader = new BufferedReader(new FileReader("EmailChart.csv"));
        ArrayList<String> sheetSideEmails = new ArrayList<>();
        ArrayList<String> sheetSideNames = new ArrayList<>();
        Emails emails = new Emails();

        String key = "";
        String value = "";

        for (long i = 0; i < 621; i++) {
            String throwawayString = emailFileReader.readLine();
            if (throwawayString != null) {
                if (throwawayString.startsWith("From: ")) {
                    value = throwawayString.substring(6, throwawayString.length()).toLowerCase().replace(" ", "");
                }
                if (throwawayString.startsWith("To: ")) {
                    if (throwawayString.contains("<")) {
                        int index = throwawayString.indexOf("<");
                        key = throwawayString.substring(4, index);
                    } else {
                        key = throwawayString.substring(4, throwawayString.length());
                    }

                    System.out.println(key + ", " + value);
                    emails.addService(key, value);
                }
            }
        }
        emailFileReader.close();
        emails.writeToCSV("EmailsSent.csv");

        int index = 0;

        for (long i = 0; i < 53; i++) {
            String throwawayString = csvFileReader.readLine();
            if (throwawayString != null) {
                index = throwawayString.indexOf(",");
                sheetSideEmails.add(throwawayString.substring(index + 1, throwawayString.length()) + "@mail.cs-georgetown.net");
                sheetSideNames.add(throwawayString.substring(0, index).toLowerCase().replace(" ", ""));
            }
        }
        csvFileReader.close();

        int violations = 0;

        for (int i = 0; i < sheetSideEmails.size(); i++) {
            ArrayList<String> x = emails.getServices(sheetSideEmails.get(i));
            for (int j = 0; j < x.size(); j++) {
                if (!x.get(j).contains(sheetSideNames.get(i))) {
                    System.out.println("Problem: " + x.get(j) + " is a service emailing " + sheetSideEmails.get(i)
                            + " without previously signing up.");
                    violations++;
                } else {
                    System.out.println("No problems yet for " + x.get(j) + " emailing " + sheetSideEmails.get(i));
                }
            }
        }
        System.out.println("Process finished with " + violations + " total violations.");
    }
}
