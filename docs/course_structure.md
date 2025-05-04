# Course Structure

The structure for a course is:

```
Course
    Module
        Lesson
            Assignment
```

The Course is the top-level entity, which contains multiple Modules. Each Module
can contain multiple Lessons, and each Lesson can have multiple Assignments,
with each level represented by a directory in the file system, except for the
last, which is a file . However, a Lesson can be combined with Assignment, if
the Lesson is just a single file. 