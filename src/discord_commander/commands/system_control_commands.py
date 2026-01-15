
    def _spawn_restart_process(self, start_script: Path) -> None:
        """Spawn the restart process with platform-specific settings."""
        project_root = start_script.parent.parent
        cmd = [sys.executable, str(start_script)]
        kwargs = {
            'cwd': str(project_root),
            'stdout': subprocess.DEVNULL,
            'stderr': subprocess.DEVNULL
        }

        if sys.platform == 'win32':
            kwargs['creationflags'] = subprocess.CREATE_NEW_CONSOLE
        else:
            kwargs['start_new_session'] = True

        subprocess.Popen(cmd, **kwargs)

    def _wait_and_log_restart(self) -> None:
        """Wait briefly and log successful restart."""
        import time
        time.sleep(2)
        self.logger.info("✅ New bot + queue processor processes spawned - current process will exit")


__all__ = ["SystemControlCommands"]

