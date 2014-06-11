#!/usr/bin/env python
import sys
import os

input_dir = sys.argv[1]
output_dir = sys.argv[2]

submit_dir = os.path.join(input_dir, 'res')
truth_dir = os.path.join(input_dir, 'ref')
history_dir = os.path.join(input_dir, 'history')

audit_score = None
audit_submission_count = 0

if not os.path.isdir(submit_dir):
    print "%s doesn't exist" % submit_dir

if os.path.isdir(history_dir):
    # read all phases and their submissions
    phases = {}

    for phase_file in os.listdir(history_dir):
        if os.path.isdir(os.path.join(history_dir, phase_file)):
            phases[phase_file] = []
            for submission_file in os.listdir(os.path.join(history_dir, phase_file)):
                if os.path.isdir(os.path.join(history_dir, phase_file, submission_file)):
                    phases[phase_file].append(submission_file)

    # create list of score files
    score_files = []

    for phase, submissions in phases.items():
        for submission in submissions:
            score_files.append(os.path.join(history_dir, phase, submission, 'output', 'scores.txt'))

    # read and save score files
    scores = []
    audit_score = 0

    for score_file in score_files:
        file_data = open(score_file).read()
        audit_score += float(file_data.split(":")[1])

    audit_submission_count = len(score_files)
    audit_score = audit_score / audit_submission_count

if os.path.isdir(submit_dir) and os.path.isdir(truth_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_filename = os.path.join(output_dir, 'scores.txt')
    output_file = open(output_filename, 'wb')

    truth_file = os.path.join(truth_dir, "truth.txt")
    truth = open(truth_file).read()

    submission_answer_file = os.path.join(submit_dir, "answer.txt")
    submission_answer = open(submission_answer_file).read()

    audit_submission_count += 1

    if truth == submission_answer:
        correct = 1.0
    else:
        correct = 0.0

    audit_score = (audit_score + correct) / audit_submission_count

    output_file.write("correct:%s\n" % correct)
    output_file.write("audit_score:%s\n" % audit_score)

    output_file.close()
