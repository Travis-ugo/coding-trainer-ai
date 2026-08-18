export function formatAuthError(err: unknown): string | null {
  if (!err) return null;
  const msg = err instanceof Error ? err.message : String(err);

  // Filter out internal database closing/connection state warnings
  if (
    msg.includes("Database is closing") ||
    msg.includes("database connection is closing") ||
    msg.includes("IDBDatabase") ||
    msg.includes("closing/hidden")
  ) {
    return null;
  }

  if (
    msg.includes("auth/user-not-found") ||
    msg.includes("auth/wrong-password") ||
    msg.includes("auth/invalid-credential")
  ) {
    return "Invalid email or password. Please check your credentials.";
  }
  if (msg.includes("auth/email-already-in-use")) {
    return "This email address is already registered. Please sign in.";
  }
  if (msg.includes("auth/weak-password")) {
    return "Password should be at least 6 characters long.";
  }
  if (msg.includes("auth/invalid-email")) {
    return "Please enter a valid email address.";
  }

  return msg;
}
