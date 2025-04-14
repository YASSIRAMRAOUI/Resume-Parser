package com.yassir.sdit.resumeparser;

import org.apache.kafka.clients.admin.NewTopic;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.kafka.config.TopicBuilder;

import static com.yassir.sdit.resumeparser.parser.common.Constants.OCR_REQUESTS_TOPIC;

@SpringBootApplication
public class ResumeParserApplication {

	public static void main(String[] args) {

		SpringApplication.run(ResumeParserApplication.class, args);
	}

	@Bean
	public NewTopic ocr_requests_topic() {
		return TopicBuilder.name(OCR_REQUESTS_TOPIC)
				.partitions(1)
				.replicas(1)
				.build();
	}

	@KafkaListener(topics = OCR_REQUESTS_TOPIC, id = "resume-parser")
	public void listen(String message) {
		System.out.println(message);
	}
}
