package com.mail;

import java.io.FileNotFoundException;
import java.io.PrintWriter;
import java.util.ArrayList;

public class Emails {
    ArrayList<ArrayList<String>> m_services = new ArrayList<>();

    public Emails() {
    }

    public void addService(String emailAddress, String service) {
        ArrayList<String> x = new ArrayList<>();
        x.add(emailAddress);
        x.add(service);
        m_services.add(x);
    }

    public ArrayList<String> getServices(String emailAddresses) {
        ArrayList<String> x = new ArrayList<>();
        for (int i = 0; i < m_services.size(); i++) {
            if (m_services.get(i).get(0).equals(emailAddresses)) {
                x.add(m_services.get(i).get(1));
            }
        }
        return x;
    }

    public void writeToCSV(String csvPath) {
        try (PrintWriter writer = new PrintWriter(csvPath)) {
            StringBuilder sb = new StringBuilder();
            for (int i = 0; i < m_services.size(); i++) {
                sb.append(m_services.get(i).get(0));
                sb.append(',');
                sb.append(m_services.get(i).get(1));
                sb.append('\n');
            }
            writer.write(sb.toString());
            System.out.println("Successfully written to CSV");
            writer.close();
        } catch (FileNotFoundException e) {
            System.out.println(e.getMessage());
        }
    }
}
