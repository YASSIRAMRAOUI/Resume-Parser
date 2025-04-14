package com.yassir.sdit.resumeparser.parser;

import com.yassir.sdit.resumeparser.parser.models.Resume;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface ResumeRepository extends JpaRepository<Resume, Long> {
}
