#include <stdio.h>
#include <time.h>

void print_clock_res(clockid_t clk_id, const char *name) {
  struct timespec res;
  clock_getres(clk_id, &res);
  printf("%s resolution: %ld seconds, %ld nanoseconds\n", name, res.tv_sec,
         res.tv_nsec);
}

void print_formatted_time(struct timespec *ts) {
  char buffer[100];
  struct tm *tm_info;

  tm_info = localtime(&ts->tv_sec); // Convert time_t seconds to struct tm
  strftime(buffer, sizeof(buffer), "%a %H:%M:%S",
           tm_info); // Format date and time

  long milliseconds =
      ts->tv_nsec / 1000000; // Convert nanoseconds to milliseconds
  long microseconds = (ts->tv_nsec % 1000000) / 1000; // Remaining microseconds
  long nanoseconds = ts->tv_nsec % 1000;              // Remaining nanoseconds

  printf("%s.%03ld,%03ld,%03ld\n", buffer, milliseconds, microseconds,
         nanoseconds);
}

int main() {
  struct timespec ts;
  if (clock_gettime(CLOCK_REALTIME, &ts) == 0) {
    printf("CLOCK_REALTIME:  ");
    print_formatted_time(&ts);
  } else {
    perror("Failed to get CLOCK_REALTIME");
  }

  if (clock_gettime(CLOCK_MONOTONIC, &ts) == 0) {
    printf("CLOCK_MONOTONIC:  %ld seconds, %ld nanoseconds\n", ts.tv_sec,
           ts.tv_nsec);
  } else {
    perror("Failed to get CLOCK_MONOTONIC");
  }
  return 0;
}
