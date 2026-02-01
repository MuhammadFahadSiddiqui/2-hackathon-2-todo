"use client";

import { Task, tasksApi } from "@/lib/api";

interface ReminderBannerProps {
  reminders: Task[];
  onDismiss: (taskId: number) => void;
  onDismissAll: () => void;
}

export function ReminderBanner({
  reminders,
  onDismiss,
  onDismissAll,
}: ReminderBannerProps) {
  if (reminders.length === 0) return null;

  const formatDeadline = (deadline: string | null) => {
    if (!deadline) return null;
    const date = new Date(deadline);
    const now = new Date();
    const diffMs = date.getTime() - now.getTime();
    const diffHours = Math.floor(diffMs / (1000 * 60 * 60));
    const diffDays = Math.floor(diffHours / 24);

    if (diffMs < 0) {
      return "Overdue!";
    } else if (diffHours < 1) {
      return "Due soon!";
    } else if (diffHours < 24) {
      return `Due in ${diffHours}h`;
    } else {
      return `Due in ${diffDays}d`;
    }
  };

  const handleDismiss = async (taskId: number) => {
    try {
      await tasksApi.acknowledgeReminder(taskId);
      onDismiss(taskId);
    } catch (err) {
      console.error("Failed to acknowledge reminder:", err);
    }
  };

  const handleDismissAll = async () => {
    try {
      await Promise.all(reminders.map((r) => tasksApi.acknowledgeReminder(r.id)));
      onDismissAll();
    } catch (err) {
      console.error("Failed to acknowledge reminders:", err);
    }
  };

  return (
    <div className="mb-6 overflow-hidden rounded-xl border border-[var(--primary-yellow)]/30 bg-[var(--primary-yellow)]/10 shadow-lg">
      <div className="flex items-center justify-between border-b border-[var(--primary-yellow)]/20 px-4 py-3">
        <div className="flex items-center gap-2">
          <svg
            className="h-5 w-5 text-[var(--primary-yellow)]"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"
            />
          </svg>
          <span className="font-semibold text-[var(--foreground)]">
            Task Reminders ({reminders.length})
          </span>
        </div>
        {reminders.length > 1 && (
          <button
            onClick={handleDismissAll}
            className="text-sm text-[var(--muted)] transition-colors hover:text-[var(--foreground)]"
          >
            Dismiss all
          </button>
        )}
      </div>
      <ul className="divide-y divide-[var(--primary-yellow)]/10">
        {reminders.map((task) => (
          <li
            key={task.id}
            className="flex items-center justify-between px-4 py-3"
          >
            <div className="flex-1 min-w-0">
              <p className="truncate font-medium text-[var(--foreground)]">
                {task.title}
              </p>
              {task.deadline && (
                <p
                  className={`text-sm ${
                    new Date(task.deadline) < new Date()
                      ? "text-[var(--error)]"
                      : "text-[var(--muted)]"
                  }`}
                >
                  {formatDeadline(task.deadline)}
                </p>
              )}
            </div>
            <button
              onClick={() => handleDismiss(task.id)}
              className="ml-4 rounded-lg p-2 text-[var(--muted)] transition-colors hover:bg-[var(--card-bg)] hover:text-[var(--foreground)]"
              aria-label="Dismiss reminder"
            >
              <svg
                className="h-4 w-4"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M6 18L18 6M6 6l12 12"
                />
              </svg>
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}
